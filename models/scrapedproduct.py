from dataclasses import dataclass

from persistence.database import Base
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from models.gpu import GPU


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

    def __init__(self, product_enum: GPU, url: str, item_price: float, availability: bool):
        self.product_id = product_enum.value
        self.url = url
        self.item_price = item_price
        self.availability = availability

    def __repr__(self):
        return str(self.__dict__)

    # def __repr__(self):
    #     return f"<ScrapedProduct id={self.product_id} url={self.url} price={self.item_price}"
