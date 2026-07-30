import asyncio
import time
from typing import List

from src.client.deribit_client import DeribitClient
from src.db.models import Price
from src.db.session import get_session, init_db
from src.tasks.celery_app import celery_app


async def _fetch_and_store() -> None:
    await init_db()
    tickers: List[str] = ["btc_usd", "eth_usd"]
    ts = int(time.time())

    async with DeribitClient() as client:
        results = []
        for ticker in tickers:
            price = await client.get_index_price(ticker)
            results.append((ticker, price))

    async with get_session() as session:
        for ticker, price in results:
            if price is None:
                continue
            session.add(Price(ticker=ticker, price=price, ts=ts))
        await session.commit()


@celery_app.task(name="src.tasks.fetch_prices.fetch_and_store_prices")
def fetch_and_store_prices() -> None:
    asyncio.run(_fetch_and_store())
