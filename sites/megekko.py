

from bs4.element import Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Megekko(Website):
    """Megekko implementation"""

    def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        return []

    def create_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        pass

    def strip_price(self, price: str) -> float:
        return 0.0

    def check_availability(self, stock: str) -> bool:
        return False
