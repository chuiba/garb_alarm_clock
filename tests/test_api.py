"""api 模块测试：用 httpx.MockTransport 模拟 B 站接口。"""

import httpx
import pytest

from garb_alarm_clock.api import (
    API_BASE,
    RECENT_RANK_ENDPOINT,
    SUIT_ENDPOINT,
    GarbAPIError,
    GarbClient,
    _safe_int,
)


def make_client(handler):
    transport = httpx.MockTransport(handler)
    return GarbClient(httpx.Client(base_url=API_BASE, transport=transport))


def suit_payload(**overrides):
    data = {
        "item": {
            "name": "测试装扮",
            "properties": {
                "fan_share_image": "https://example.com/share.png",
                "image_cover": "https://example.com/cover.png",
                "sale_quantity": "1000",
            },
        },
        "fan_user": {"avatar": "https://example.com/avatar.png"},
        "sale_surplus": 400,
    }
    data.update(overrides)
    return {"code": 0, "message": "0", "data": data}


def test_fetch_info_computes_number_from_stock():
    def handler(request):
        assert request.url.path == SUIT_ENDPOINT
        assert request.url.params["item_id"] == "4389"
        return httpx.Response(200, json=suit_payload())

    with make_client(handler) as client:
        info = client.fetch_info("4389")

    assert info.name == "测试装扮"
    assert info.image_url == "https://example.com/share.png"
    assert info.avatar_url == "https://example.com/avatar.png"
    assert info.sale_surplus == 400
    assert info.sale_quantity == 1000
    assert info.fan_number == 600


def test_fetch_info_falls_back_to_rank_when_stock_missing():
    def handler(request):
        if request.url.path == SUIT_ENDPOINT:
            return httpx.Response(200, json=suit_payload(sale_surplus=None))
        assert request.url.path == RECENT_RANK_ENDPOINT
        return httpx.Response(
            200,
            json={"code": 0, "data": {"rank": [{"number": "notanumber"}, {"number": 123}]}},
        )

    with make_client(handler) as client:
        info = client.fetch_info("4389")

    assert info.fan_number == 123


def test_fetch_info_uses_cover_when_share_image_missing():
    def handler(request):
        payload = suit_payload()
        del payload["data"]["item"]["properties"]["fan_share_image"]
        return httpx.Response(200, json=payload)

    with make_client(handler) as client:
        info = client.fetch_info("4389")

    assert info.image_url == "https://example.com/cover.png"


def test_fetch_info_raises_on_api_error_code():
    def handler(request):
        return httpx.Response(200, json={"code": -412, "message": "请求被拦截"})

    with make_client(handler) as client, pytest.raises(GarbAPIError, match="请求被拦截"):
        client.fetch_info("4389")


def test_fetch_info_raises_on_http_error():
    def handler(request):
        return httpx.Response(500)

    with make_client(handler) as client, pytest.raises(httpx.HTTPStatusError):
        client.fetch_info("4389")


def test_fetch_fan_number_returns_zero_for_empty_rank():
    def handler(request):
        return httpx.Response(200, json={"code": 0, "data": {"rank": []}})

    with make_client(handler) as client:
        assert client.fetch_fan_number("4389") == 0


def test_fetch_fan_number_handles_missing_data():
    def handler(request):
        return httpx.Response(200, json={"code": 0})

    with make_client(handler) as client:
        assert client.fetch_fan_number("4389") == 0


def test_fetch_image_returns_bytes():
    def handler(request):
        assert request.url == "https://example.com/avatar.png"
        return httpx.Response(200, content=b"fake-image")

    with make_client(handler) as client:
        assert client.fetch_image("https://example.com/avatar.png") == b"fake-image"


@pytest.mark.parametrize(
    ("value", "expected"),
    [("42", 42), (42, 42), (None, None), ("abc", None), ("", None)],
)
def test_safe_int(value, expected):
    assert _safe_int(value) == expected
