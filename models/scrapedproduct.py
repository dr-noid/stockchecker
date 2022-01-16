from dataclasses import dataclass


@dataclass
class ScrapedProduct():
    product_id: int
    url: str
    store_price: float
    availability: bool

    # def __init__(self, product_id: int, url: str, store_price: float, availability: bool):
    #     self.product_id = product_id
    #     self.url = url
    #     self.store_price = store_price
    #     self.availability = availability
