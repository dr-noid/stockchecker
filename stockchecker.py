"""
This module has high level funcionality to do stock checking.
And keep clutter out of app.py of course.
"""

import asyncio
from os import environ
from timeit import default_timer as timer

from pywhatkit.whats import sendwhatmsg_to_group_instantly

from models.product import Product
from models.scrapedproduct import ScrapedProduct
from models.website import Website
from persistence import database
from sites.alternate import Alternate
from sites.azerty import Azerty
from sites.megekko import Megekko

WHATSAPP_GROUP_ID = environ.get("WHATSAPP_GROUP_ID")


async def run(websites: list[Website]):
    coroutines = [website.run() for website in websites]

    start = timer()
    await asyncio.gather(*coroutines)
    end = timer()
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


def send_notif(product: ScrapedProduct) -> None:
    p = product
    msg = f"{p.url}\nPrice: {p.item_price}"
    sendwhatmsg_to_group_instantly(
        group_id=WHATSAPP_GROUP_ID, message=msg, wait_time=7, tab_close=True, close_time=0)


def send_notifications() -> None:
    products: list[ScrapedProduct] = database.session.query(
        ScrapedProduct).all()
    print(len(products))
    for p in products:
        print(p)
        send_notif(p)


if __name__ == "__main__":
    pass
