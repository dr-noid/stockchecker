import stockchecker
from models.scrapedproduct import ScrapedProduct
from utilities import json_parser, launch_args


def main():
    settings = launch_args.parse_args()

    if settings["db_reset"]:
        print("DB flushed")
        stockchecker.db_init()

    prices = json_parser.get_prices("prices.json")
    products = json_parser.get_products()

    stockchecker.add_prices_to_products(products, prices)

    website_list = stockchecker.create_website_list()

    stockchecker.distribute_products(website_list, products)

    stockchecker.run(website_list)

    stockchecker.save_all(website_list)


if __name__ == "__main__":
    main()
