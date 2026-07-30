from datetime import date, datetime
from typing import List

from sqlalchemy import select

from src.db.models import Price
from src.db.session import get_session


class PriceService:
    async def get_prices_by_ticker(self, ticker: str) -> List[Price]:
        async with get_session() as session:
            result = await session.execute(select(Price).where(Price.ticker == ticker).order_by(Price.ts.asc()))
            return list(result.scalars().all())

    async def get_latest_price(self, ticker: str) -> Price | None:
        async with get_session() as session:
            result = await session.execute(
                select(Price).where(Price.ticker == ticker).order_by(Price.ts.desc(), Price.id.desc()).limit(1)
            )
            return result.scalar_one_or_none()

    async def get_prices_by_date(self, ticker: str, target_date: date) -> List[Price]:
        start = int(datetime.combine(target_date, datetime.min.time()).timestamp())
        end = int(datetime.combine(target_date, datetime.max.time()).timestamp())
        async with get_session() as session:
            result = await session.execute(
                select(Price)
                .where(Price.ticker == ticker)
                .where(Price.ts >= start)
                .where(Price.ts <= end)
                .order_by(Price.ts.asc())
            )
            return list(result.scalars().all())
