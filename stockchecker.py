from models.product import Product
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


if __name__ == "__main__":
    pass
