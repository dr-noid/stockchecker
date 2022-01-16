from typing import Any

from bs4.element import NavigableString, ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Alternate(Website):
    """Alternate implementation"""

    def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        page_source = self.request(product.url)

        soup = self.soupify(page_source)

        listings_container: Tag | NavigableString | None = soup.find(
            "div", attrs={"class": "grid-container listing"})

        # We need a Tag object to continue the process
        if not isinstance(listings_container, Tag):
            raise TypeError("listings_container must be of type Tag")

        html_items: ResultSet[Any] = listings_container.find_all(
            "a", attrs={"class": "productBox"})

        scraped_products = []

        for item in html_items:
            scraped_products.append(
                self.create_product(product.product_id, item))

        return scraped_products

    def create_product(self, product_id: int, item: Tag) -> ScrapedProduct:
        name = item.find("div", attrs={"class": "product-name"})
        price = item.find("span", attrs={"class": "price"})
        stock = item.find("span", attrs={"class": "font-weight-bold"})
        url = item["href"]

        if not isinstance(name, Tag) or not isinstance(price, Tag) \
                or not isinstance(stock, Tag) or not isinstance(url, str):
            raise TypeError("Incorrect type")

        return ScrapedProduct(
            product_id=product_id,
            url=url,
            store_price=self.strip_price(price.text),
            availability=self.availability(stock.text))

    def strip_price(self, price: str) -> float:
        sanitized_price: str = price.strip("€").strip(
            " ").replace(".", "").replace(",", ".")

        return float(sanitized_price)

    def availability(self, stock: str) -> bool:
        return stock.__contains__("Op voorraad")
