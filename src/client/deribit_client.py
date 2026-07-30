import asyncio
from typing import Optional

import aiohttp


class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2"

    def __init__(self, session: Optional[aiohttp.ClientSession] = None, timeout: int = 10) -> None:
        self._external_session = session
        self._session: Optional[aiohttp.ClientSession] = session
        self._timeout = timeout

    async def __aenter__(self) -> "DeribitClient":
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._external_session is None and self._session is not None:
            await self._session.close()
            self._session = None

    async def get_index_price(self, index_name: str) -> Optional[float]:
        session = self._session
        should_close_session = False

        if session is None:
            session = aiohttp.ClientSession()
            self._session = session
            should_close_session = True

        try:
            url = f"{self.BASE_URL}/public/get_index"
            params = {"index_name": index_name}
            async with session.get(url, params=params, timeout=self._timeout) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                result = data.get("result") or {}
                index_price = result.get("index")
                if index_price is None:
                    return None
                return float(index_price)
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
            return None
        finally:
            if should_close_session:
                await session.close()
                self._session = None

