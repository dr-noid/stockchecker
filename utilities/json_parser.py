import json
import os

from models.product import Product

PRODUCT_DIR = "products/"


def parse_json(filename: str) -> list[dict[str, str | int]]:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file).values()
        return list(data)[0]


def get_product_files() -> list[str]:
    files = os.listdir("products")

    try:
        files.remove("template.json")
    finally:
        return files


def get_products() -> list[Product]:
    """Returns `Product` list parsed from json files"""
    files = get_product_files()
    product_list = []
    for filename in files:
        data = parse_json(PRODUCT_DIR + filename)
        for product in data:
            id = product["id"]
            url = product["url"]

            if not isinstance(id, int) or not isinstance(url, str):
                raise TypeError("JSON parse error")

            product_list.append(Product(id, url))

    return product_list


def get_prices(filename: str) -> dict[int, int]:
    """Returns a dict with product ids as keys and prices as values"""

    json_prices = parse_json(filename)

    if json_prices is None:
        raise ValueError("No prices, check prices.json")

    price_dict: dict[int, int] = {}

    for product_price in json_prices:
        price = product_price["price"]
        id = product_price["id"]

        if not isinstance(id, int) or not isinstance(price, int):
            raise TypeError("JSON parse error")

        price_dict[id] = price

    return price_dict
