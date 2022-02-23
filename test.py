import stockchecker
from models.website import Website
from sites.megekko import Megekko
from utilities import json_parser


def main():
    prices = json_parser.get_prices("prices.json")
    products = json_parser.get_products("products.json")

    stockchecker.add_prices_to_products(products, prices)

    website_list: list[Website] = [Megekko()]

    stockchecker.distribute_products(website_list, products)

    print("running now")
    print(website_list[0])
    stockchecker.run(website_list)


if __name__ == "__main__":
    main()
