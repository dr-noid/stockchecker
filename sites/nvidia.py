from typing import Any

from bs4.element import ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Nvidia(Website):
    """Nvidia Implementation"""

    async def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        soup = await self.get_soup(product.url)

        html_items: ResultSet[Any] = soup.find_all(
            "div", attrs={"class": "product-details-list-tile"})

        scraped_products = []

        for item in html_items:
            scraped_product = self.find_product(product, item)
            if self.validate_scraped(scraped_product, product):
                scraped_products.append(scraped_product)

        return scraped_products

    def find_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        name_element = item.find("h2", attrs={"class": "name"})
        a_element = item.find("a", attrs={"class": "featured-buy-link"})
        stock_element = a_element
        price_element = item.find("div", attrs={"class": "price"})

        print(name_element.text)
        print(a_element['href'])
        print(stock_element.text)
        print(price_element.text)

        return None

        name = name_element.text
        url = a_element["href"]

        if not isinstance(name, str) or not isinstance(url, str):
            raise TypeError("Incorrect type")

        url = "https://www.megekko.nl" + url
        price = self.strip_price(price_element.text)
        availability = self.check_availability(stock_element.text)

        return ScrapedProduct(product.product_enum, url, price, availability)

    def strip_price(self, price: str) -> float:
        return float(price.strip(",-"))
