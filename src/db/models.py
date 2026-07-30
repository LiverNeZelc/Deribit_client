from sqlalchemy import BigInteger, Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(length=32), nullable=False, index=True)
    price = Column(Float, nullable=False)
    ts = Column(BigInteger, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Price id={self.id} ticker={self.ticker} price={self.price} ts={self.ts}>"
