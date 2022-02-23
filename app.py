import stockchecker
from models.scrapedproduct import ScrapedProduct
from utilities import json_parser


def main():
    stockchecker.db_init()

    prices = json_parser.get_prices("prices.json")
    products = json_parser.get_products()

    stockchecker.add_prices_to_products(products, prices)

    website_list = stockchecker.create_website_list()

    stockchecker.distribute_products(website_list, products)

    print("running now")
    stockchecker.run(website_list)

    scraped_products: list[ScrapedProduct] = []
    for website in website_list:
        scraped_products.extend(website.scraped_products)

    print(f"Amount of scraped products: {len(scraped_products)}")

    stockchecker.save(scraped_products)


if __name__ == "__main__":
    main()
