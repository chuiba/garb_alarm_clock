"""Helpers for fetching Bilibili garb data."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Tuple

import requests

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
DEFAULT_TIMEOUT = 10  # seconds

_SESSION = requests.Session()
_SESSION.headers.update(DEFAULT_HEADERS)


class GarbAPIError(RuntimeError):
    """Raised when the garb API responds with an unexpected payload."""


def _request_json(endpoint: str, *, params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a GET request against the garb API and return the JSON payload."""
    url = f"{API_BASE}{endpoint}"
    response = _SESSION.get(url, params=params, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    if payload.get("code") != 0:
        raise GarbAPIError(payload.get("message", "garb api error"))
    return payload.get("data", {})


def _safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _first_number(rank_list: Iterable[Dict[str, Any]]) -> Optional[int]:
    for item in rank_list:
        number = _safe_int(item.get("number"))
        if number is not None:
            return number
    return None


def get_garb_number(garb_id: Any) -> int:
    """Fetch the latest fan number for a given garb."""
    data = _request_json(RECENT_RANK_ENDPOINT, params={"item_id": garb_id})
    rank = data.get("rank") or []
    number = _first_number(rank)
    return number if number is not None else 0


def get_garb_info(garb_id: Any) -> Tuple[str, str, str, str, str, str]:
    """Return metadata required by the UI for the given garb item."""
    data = _request_json(SUIT_ENDPOINT, params={"item_id": garb_id})

    item = data.get("item", {})
    properties = item.get("properties", {})
    fan_user = data.get("fan_user", {})

    name = item.get("name", "")
    image = (
        properties.get("fan_share_image")
        or properties.get("image_cover")
        or ""
    )
    avatar = fan_user.get("avatar", "")
    surplus = data.get("sale_surplus")
    quantity = properties.get("sale_quantity")

    quantity_val = _safe_int(quantity)
    surplus_val = _safe_int(surplus)

    if quantity_val is not None and surplus_val is not None and quantity_val >= 0:
        number = quantity_val - surplus_val
    else:
        number = get_garb_number(garb_id)

    return (
        name,
        image,
        avatar,
        str(surplus if surplus is not None else ""),
        str(quantity if quantity is not None else ""),
        str(number),
    )
