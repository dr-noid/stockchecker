from typing import Any

from bs4.element import NavigableString, ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Alternate(Website):
    """Alternate implementation"""

    def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        soup = self.get_soup(product.url, delay=1)

        listings_container: Tag | NavigableString | None = soup.find(
            "div", attrs={"class": "grid-container listing"})

        # We need a Tag object to continue the process
        if not isinstance(listings_container, Tag):
            raise TypeError("listings_container must be of type Tag")

        html_items: ResultSet[Any] = listings_container.find_all(
            "a", attrs={"class": "productBox"})

        scraped_products = []

        for item in html_items:
            scraped_product = self.create_product(product, item)
            if self.validate_scraped(scraped_product, product):
                scraped_products.append(scraped_product)

        return scraped_products

    def create_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        name = item.find("div", attrs={"class": "product-name"})
        price = item.find("span", attrs={"class": "price"})
        stock = item.find("span", attrs={"class": "font-weight-bold"})
        url = item["href"]

        if not isinstance(name, Tag) or not isinstance(price, Tag) \
                or not isinstance(stock, Tag) or not isinstance(url, str):
            raise TypeError("Incorrect type")

        price = self.strip_price(price.text)
        availability = self.check_availability(stock.text)

        scraped_product = ScrapedProduct(
            product_id=product.product_id,
            url=url,
            item_price=price,
            availability=availability)

        return scraped_product

    def strip_price(self, price: str) -> float:
        sanitized_price: str = price.strip("€").strip(
            " ").replace(".", "").replace(",", ".")

        return float(sanitized_price)

    def check_availability(self, stock: str) -> bool:
        return stock in ["Op voorraad", "Binnenkort op voorraad"]
