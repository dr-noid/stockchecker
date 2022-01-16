"""
Product module containing Product class
"""


class Product():
    product_id: int
    url: str
    price_threshold: int

    def __init__(self, product_id: int, url: str):
        self.product_id = product_id
        self.url = url

    def __repr__(self):
        return f"{__class__.__name__}({self.product_id}, {self.url})"
