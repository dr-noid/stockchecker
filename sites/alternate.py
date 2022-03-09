from typing import Any

from bs4.element import NavigableString, ResultSet, Tag
from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website


class Alternate(Website):
    """Alternate implementation"""
    compatible_stocks = ["Op voorraad", "Binnenkort op voorraad"]

    async def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        soup = await self.get_soup(product.url)

        listings_container: Tag | NavigableString | None = soup.find(
            "div", attrs={"class": "grid-container listing"})

        # We need a Tag object to continue the process
        if not isinstance(listings_container, Tag):
            # TODO: change print calls to logging
            self.log(f"cant find listings Product({product.url})")
            return []

        html_items: ResultSet[Any] = listings_container.find_all(
            "a", attrs={"class": "productBox"})

        scraped_products = []

        for item in html_items:
            scraped_product = self.find_product(product, item)
            if self.validate_scraped(scraped_product, product):
                scraped_products.append(scraped_product)

        return scraped_products

    def find_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        name_element = item.find("div", attrs={"class": "product-name"})
        price_element = item.find("span", attrs={"class": "price"})
        stock_element = item.find("span", attrs={"class": "font-weight-bold"})
        url = item["href"]

        if not isinstance(name_element, Tag) or not isinstance(price_element, Tag) \
                or not isinstance(stock_element, Tag) or not isinstance(url, str):
            raise TypeError("Incorrect type")

        price = self.strip_price(price_element.text)
        availability = self.check_availability(stock_element.text)

        return ScrapedProduct(product.product_enum, url, price, availability)

    def strip_price(self, price: str) -> float:
        sanitized_price: str = price.strip("€").strip(
            " ").replace(".", "").replace(",", ".")

        return float(sanitized_price)

    def check_availability(self, stock: str) -> bool:
        for x in self.compatible_stocks:
            if stock.find(x) != -1:
                return True
        return False
