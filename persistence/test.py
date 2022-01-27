from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Float, Integer, String

import database


@dataclass
class ScrapedProduct(database.Base):
    __tablename__ = "scrapedproduct"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    item_price = Column(Float, nullable=False)
    availability = Column(Boolean, nullable=False)

    def __init__(self, product_id, url, item_price, availability):
        self.product_id = product_id
        self.url = url
        self.item_price = item_price
        self.availability = availability
        database.add_metadata(self)


database.add_metadata(ScrapedProduct)


for i in range(20):
    o = ScrapedProduct(i, "url", 99.9, True)
    database.save(o)
