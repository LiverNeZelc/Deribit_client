from datetime import date

from fastapi import FastAPI, HTTPException, Query

from src.db.session import init_db
from src.services.price_service import PriceService

app = FastAPI(title="Deribit client API")
price_service = PriceService()


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


@app.get("/prices")
async def get_prices(ticker: str = Query(..., description="Ticker like btc_usd or eth_usd")):
    return await price_service.get_prices_by_ticker(ticker)


@app.get("/prices/latest")
async def get_latest_price(ticker: str = Query(..., description="Ticker like btc_usd or eth_usd")):
    price = await price_service.get_latest_price(ticker)
    if price is None:
        raise HTTPException(status_code=404, detail="No data found")
    return price


@app.get("/prices/by-date")
async def get_prices_by_date(
    ticker: str = Query(..., description="Ticker like btc_usd or eth_usd"),
    date_value: date = Query(..., alias="date"),
):
    return await price_service.get_prices_by_date(ticker, date_value)
