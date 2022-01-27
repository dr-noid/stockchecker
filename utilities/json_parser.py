import json

from models.product import Product


def parse_json_file(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def get_products(filename: str) -> list[Product]:
    """returns a Product list parsed from a json file"""

    data = parse_json_file(filename)

    json_products: list = data['products']

    if json_products is None:
        raise ValueError("No products, check products.json")

    product_list = []

    for product in json_products:
        product_list.append(
            Product(product_id=product["id"], url=product["url"]))

    return product_list


def get_prices(filename: str) -> dict[int, int]:
    """Returns a dict with product ids as keys and prices as values"""

    data = parse_json_file(filename)

    json_prices: list = data["prices"]

    if json_prices is None:
        raise ValueError("No prices, check prices.json")

    price_dict: dict[int, int] = {}

    for json_price in json_prices:
        product_id: int = json_price['id']
        price: int = json_price['price']

        price_dict[product_id] = price

    return price_dict
