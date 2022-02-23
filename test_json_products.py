import json
import os

from models.product import Product

PRODUCT_DIR = "products/"


def get_product_files() -> list[str]:
    files = os.listdir("products")

    try:
        files.remove("template.json")
    finally:
        return files


def open_json(filename: str) -> list[dict[str, str | int]]:
    with open(PRODUCT_DIR + filename, "r", encoding="utf-8") as file:
        data = json.load(file).values()
        return list(data)[0]


def get_products(filenames: list[str]) -> list[Product]:
    product_list = []
    for filename in filenames:
        data = open_json(filename)
        for product in data:
            id = product["id"]
            url = product["url"]

            if not isinstance(id, int) or not isinstance(url, str):
                raise TypeError("JSON parse error")

            product_list.append(Product(id, url))

    return product_list


if __name__ == '__main__':
    product_files = get_product_files()
    products = get_products(product_files)
