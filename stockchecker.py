import jsons

from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website
from sites.alternate import Alternate
from sites.azerty import Alternate


def run(websites: list[Website]):
    for website in websites:
        website.run()


def create_website_list() -> list[Website]:
    website_list: list[Website] = [
        Alternate(),
        Alternate()
    ]
    return website_list


def distribute_products(websites: list[Website],
                        products: list[Product]) -> None:
    """
    Goes through the products list and finds matching
    sites to add the products to.
    """
    for product in products:
        for website in websites:
            if website.name() in product.url:
                website.products.append(product)


def add_prices_to_products(products: list[Product], prices: dict) -> None:
    for product in products:
        product.price_threshold = prices[product.product_id]


def save_to_json(product: ScrapedProduct) -> None:
    with open("scraped.json", "a", encoding="utf-8") as file:
        file.write(jsons.dumps(product))


if __name__ == "__main__":
    pass
