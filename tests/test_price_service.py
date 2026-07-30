from contextlib import asynccontextmanager

import pytest

from src.db.models import Price
from src.services.price_service import PriceService


class FakeResult:
    def __init__(self, values):
        self._values = values

    def scalars(self):
        return self

    def all(self):
        return self._values

    def scalar_one_or_none(self):
        return self._values[0] if self._values else None


class FakeSession:
    def __init__(self, values):
        self._values = values

    async def execute(self, query):
        return FakeResult(self._values)


@pytest.mark.asyncio
async def test_get_prices_by_ticker_returns_rows(monkeypatch):
    stored_rows = [Price(ticker="btc_usd", price=100.0, ts=1)]

    @asynccontextmanager
    async def fake_get_session():
        yield FakeSession(stored_rows)

    monkeypatch.setattr("src.services.price_service.get_session", fake_get_session)

    service = PriceService()
    result = await service.get_prices_by_ticker("btc_usd")

    assert len(result) == 1
    assert result[0].ticker == "btc_usd"
    assert result[0].price == 100.0


@pytest.mark.asyncio
async def test_get_latest_price_returns_latest_row(monkeypatch):
    stored_rows = [Price(ticker="eth_usd", price=2000.0, ts=2)]

    @asynccontextmanager
    async def fake_get_session():
        yield FakeSession(stored_rows)

    monkeypatch.setattr("src.services.price_service.get_session", fake_get_session)

    service = PriceService()
    result = await service.get_latest_price("eth_usd")

    assert result is not None
    assert result.ticker == "eth_usd"
    assert result.price == 2000.0
