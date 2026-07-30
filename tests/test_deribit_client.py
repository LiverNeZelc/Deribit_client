from unittest.mock import AsyncMock

import pytest

from src.client.deribit_client import DeribitClient


class FakeResponse:
    def __init__(self, status, payload=None):
        self.status = status
        self._payload = payload or {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def json(self):
        return self._payload


class FakeSession:
    def __init__(self, response):
        self._response = response

    def get(self, *args, **kwargs):
        return self._response


@pytest.mark.asyncio
async def test_get_index_price_returns_float_when_response_ok():
    response = FakeResponse(200, {"result": {"index": 123.45}})
    session = FakeSession(response)

    client = DeribitClient(session=session, timeout=5)
    price = await client.get_index_price("btc_usd")

    assert price == 123.45


@pytest.mark.asyncio
async def test_get_index_price_returns_none_on_http_error():
    response = FakeResponse(500)
    session = FakeSession(response)

    client = DeribitClient(session=session, timeout=5)
    price = await client.get_index_price("btc_usd")

    assert price is None
