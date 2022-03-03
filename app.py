import asyncio

from utilities import args_parser, json_parser


def main():
    settings = args_parser.parse_args()

    import stockchecker

    if settings["db_reset"]:
        print("DB flushed")
        stockchecker.db_init()

    prices = json_parser.get_prices("prices.json")
    products = json_parser.get_products()

    stockchecker.add_prices_to_products(products, prices)

    website_list = stockchecker.create_website_list()

    stockchecker.distribute_products(website_list, products)

    asyncio.run(stockchecker.run(website_list))

    if settings["notifs"]:
        stockchecker.send_notifications()


if __name__ == "__main__":
    main()
