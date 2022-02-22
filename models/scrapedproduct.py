from dataclasses import dataclass

from persistence.database import Base
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func


@dataclass
class ScrapedProduct(Base):
    __tablename__ = "scrapedproduct"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    item_price = Column(Float, nullable=False)
    availability = Column(Boolean, nullable=False)
    time_created = Column(DateTime(timezone=True), nullable=False,
                          server_default=func.now())

    def __init__(self, product_id: int, url: str, item_price: float, availability: bool):
        self.product_id = product_id
        self.url = url
        self.item_price = item_price
        self.availability = availability

    def __repr__(self):
        return f"<ScrapedProduct id={self.product_id} url={self.url} price={self.item_price}"
