"""
This module has high level funcionality to do stock checking.
And keep clutter out of app.py of course.
"""

from timeit import default_timer as timer

from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website
from persistence import database
from sites.alternate import Alternate
from sites.azerty import Azerty
from sites.megekko import Megekko


def run(websites: list[Website]):
    for website in websites:
        print(f"Scraping {website.name()}...")
        start = timer()
        website.run()
        end = timer()
        print(f"Done, {len(website.scraped_products)} products scraped")
        print(f"Time: {round(end - start)} seconds\n")
    print(f"total products scraped: {saved_products}")


def create_website_list(price_filter: bool = True, availability_filter: bool = True) -> list[Website]:
    """
    Create a list with all of the currently implemented websites using 
    the provided arguments and return it
    """
    website_list: list[Website] = [
        Alternate(),
        Azerty(),
        Megekko()
    ]
    # If any of the arguments are provided as False we change the all the websites accordingly
    if not price_filter or not availability_filter:
        for website in website_list:
            website.price_filter = price_filter
            website.availability_filter = availability_filter

    return website_list


def distribute_products(websites: list[Website], products: list[Product]) -> None:
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


def db_init() -> None:
    database.init()
    database.add_metadata(ScrapedProduct)


saved_products = 0


def save(scraped_product: ScrapedProduct) -> None:
    database.save(scraped_product)
    global saved_products
    saved_products += 1


def save_products(scraped_products: list[ScrapedProduct]) -> None:
    for scraped_product in scraped_products:
        save(scraped_product)


if __name__ == "__main__":
    pass
