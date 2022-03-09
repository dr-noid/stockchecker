from typing import Any

from bs4.element import ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Coolblue(Website):
    """Coolblue implementation"""
    compatible_stocks = ["Morgen bezorgd"]

    async def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        soup = await self.get_soup(product.url)

        html_items: ResultSet[Any] = soup.find_all(
            "div", attrs={"class": "product-card"})

        scraped_products = []

        for item in html_items:
            scraped_product = self.find_product(product, item)
            if self.validate_scraped(scraped_product, product):
                scraped_products.append(scraped_product)

        return scraped_products

    def find_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        name_element = item.find("h3", attrs={"class": "color--link"})
        a_element = item.find("a", attrs={"class": "link"})
        stock_element = item.find(
            "span", attrs={"class": "icon-with-text__text"})
        price_element = item.find(
            "strong", attrs={"class": "sales-price__current"})

        name = name_element.text if isinstance(name_element, Tag) else None
        url = a_element.get("href", None) if isinstance(
            a_element, Tag) else None
        price = self.strip_price(price_element.text) if isinstance(
            price_element, Tag) else None
        availability = self.check_availability(
            stock_element.text) if isinstance(stock_element, Tag) else None

        # Very Pythonic I know thank you.
        if url is not None and price is not None and availability is not None:
            url = f"https://www.coolblue.nl{url}"
            return ScrapedProduct(product.product_enum, url, price, availability)

        return None

    def strip_price(self, price: str) -> float:
        return float(price.strip(",-"))

    def check_availability(self, stock: str) -> bool:
        for x in self.compatible_stocks:
            if stock.find(x) != -1:
                return True
        return False
