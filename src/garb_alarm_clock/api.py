"""B 站装扮接口客户端。

B 站在 2023 年之后对装扮接口增加了浏览器校验，请求必须携带
``User-Agent``、``Origin``、``Referer`` 头，否则会返回 412。
二次开发时请保留 ``DEFAULT_HEADERS`` 中的这些字段。
"""

from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType
from typing import Any

import httpx

API_BASE = "https://api.bilibili.com"
SUIT_ENDPOINT = "/x/garb/mall/item/suit/v2"
RECENT_RANK_ENDPOINT = "/x/garb/rank/fan/recent"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bilibili.com",
    "Origin": "https://www.bilibili.com",
}
DEFAULT_TIMEOUT = 10.0  # 秒


class GarbAPIError(RuntimeError):
    """装扮接口返回了异常状态码或无法解析的数据。"""


@dataclass(frozen=True, slots=True)
class GarbInfo:
    """界面展示所需的装扮信息。"""

    name: str
    image_url: str
    avatar_url: str
    sale_surplus: int | None
    sale_quantity: int | None
    fan_number: int


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class GarbClient:
    """装扮相关接口的同步客户端，可复用连接。"""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(
            base_url=API_BASE,
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> GarbClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def _get_data(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        response = self._client.get(endpoint, params=params)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise GarbAPIError(payload.get("message") or "garb api error")
        return payload.get("data") or {}

    def fetch_fan_number(self, item_id: str | int) -> int:
        """从最近购买榜中取最新的粉丝编号，取不到时返回 0。"""
        data = self._get_data(RECENT_RANK_ENDPOINT, params={"item_id": item_id})
        for entry in data.get("rank") or []:
            number = _safe_int(entry.get("number"))
            if number is not None:
                return number
        return 0

    def fetch_info(self, item_id: str | int) -> GarbInfo:
        """拉取装扮的完整信息。

        优先用 ``sale_quantity - sale_surplus`` 推算当前编号，
        推算不出来时回退到最近购买榜。
        """
        data = self._get_data(SUIT_ENDPOINT, params={"item_id": item_id})
        item = data.get("item") or {}
        properties = item.get("properties") or {}
        fan_user = data.get("fan_user") or {}

        surplus = _safe_int(data.get("sale_surplus"))
        quantity = _safe_int(properties.get("sale_quantity"))
        if quantity is not None and surplus is not None and quantity >= 0:
            fan_number = quantity - surplus
        else:
            fan_number = self.fetch_fan_number(item_id)

        return GarbInfo(
            name=item.get("name") or "",
            image_url=properties.get("fan_share_image") or properties.get("image_cover") or "",
            avatar_url=fan_user.get("avatar") or "",
            sale_surplus=surplus,
            sale_quantity=quantity,
            fan_number=fan_number,
        )

    def fetch_image(self, url: str) -> bytes:
        """下载头像或背景图，返回原始字节。"""
        response = self._client.get(url)
        response.raise_for_status()
        return response.content
