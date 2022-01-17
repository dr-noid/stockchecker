from dataclasses import dataclass


@dataclass
class ScrapedProduct():
    product_id: int
    url: str
    item_price: float
    availability: bool
