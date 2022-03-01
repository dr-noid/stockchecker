from typing import Any

from bs4.element import ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Azerty(Website):
    """Azerty implementation"""

    async def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        soup = await self.get_soup(product.url)

        html_items: ResultSet[Any] = soup.find_all(
            "div", attrs={"class": "item_container default_view"}
        )

        scraped_products = []

        for item in html_items:
            scraped_product = self.find_product(product, item)
            if self.validate_scraped(scraped_product, product):
                scraped_products.append(scraped_product)

        return scraped_products

    def find_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        a_element = item.find("a", attrs={"class": "item-img"}, recursive=True)
        price_element = item.find("span", attrs={"class": "price"})
        stock_element = item.find("span", attrs={"class": "stock_desc"})

        if not isinstance(a_element, Tag) or not isinstance(price_element, Tag) \
                or not isinstance(stock_element, Tag):
            raise TypeError("Incorrect type")

        name = a_element["title"]
        url = a_element["href"]

        if not isinstance(name, str) or not isinstance(url, str):
            raise TypeError("Incorrect type")

        url = "https://www.azerty.nl/" + url
        price = self.strip_price(price_element.text)
        availability = self.check_availability(stock_element.text)

        return ScrapedProduct(product.product_id, url, price, availability)

    def strip_price(self, price: str) -> float:
        sanitized_price: str = price.replace(",", ".")
        return float(sanitized_price)

    def check_availability(self, stock: str) -> bool:
        return stock.__contains__("Volgende werkdag in huis")
