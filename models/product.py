"""
Product module containing Product class
"""
from models.gpu import GPU


class Product():
    product_enum: GPU
    url: str
    price_threshold: int

    def __init__(self, product_id: int, url: str):
        self.product_enum = GPU(product_id)
        self.url = url

    def __repr__(self):
        return f"{__class__.__name__}({self.product_enum}, {self.url})"
