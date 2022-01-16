from typing import Any

from bs4.element import ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Alternate(Website):
    """Azerty implementation"""

    def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        page_source = self.request(product.url, delay=5)

        soup = self.soupify(page_source)

        html_items: ResultSet[Any] = soup.find_all(
            "div", attrs={"class": "item_container default_view"}
        )

        scraped_products = []

        for item in html_items:
            scraped_products.append(
                self.create_product(product.product_id, item))

        return scraped_products

    def create_product(self, product_id: int, item: Tag) -> ScrapedProduct:
        a_element = item.find("a", attrs={"class": "item-img"}, recursive=True)
        price_element = item.find("span", attrs={"class": "price"})
        stock_element = item.find("span", attrs={"class": "stock_desc"})

        if not isinstance(a_element, Tag) or not isinstance(price_element, Tag) \
                or not isinstance(stock_element, Tag):
            raise TypeError("Incorrect type")

        name = a_element["title"]
        price = price_element.text
        url = a_element["href"]
        stock = stock_element.text

        if not isinstance(name, str) or not isinstance(url, str):
            raise TypeError("Incorrect type")

        scraped_product = ScrapedProduct(
            product_id=product_id,
            url="https://azerty.nl/" + url,
            store_price=self.strip_price(price),
            availability=self.availability(stock))

        return scraped_product

    def strip_price(self, price: str) -> float:
        sanitized_price: str = price.replace(",", ".")
        return float(sanitized_price)

    def availability(self, stock: str) -> bool:
        return stock.__contains__("Volgende werkdag in huis")
