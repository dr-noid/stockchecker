from dataclasses import dataclass

from persistence.database import Base, add_metadata
from sqlalchemy import Boolean, Column, Float, Integer, String


@dataclass
class ScrapedProduct(Base):
    __tablename__ = "scrapedproduct"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    item_price = Column(Float, nullable=False)
    availability = Column(Boolean, nullable=False)

    def __init__(self, product_id: int, url: str, item_price: float, availability: bool):
        self.product_id = product_id
        self.url = url
        self.item_price = item_price
        self.availability = availability

    def __repr__(self):
        return f"<ScrapedProduct id={self.product_id} url={self.url} price={self.item_price}"

# @dataclass
# class ScrapedProduct(Base):
#     product_id: int
#     url: str
#     item_price: float
#     availability: bool
