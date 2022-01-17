import stockchecker
from models.scrapedproduct import ScrapedProduct
from utilities import json_parser


def main():
    product_data = json_parser.parse_json_file("products.json")
    price_data = json_parser.parse_json_file("prices.json")

    prices = json_parser.get_prices(price_data)
    products = json_parser.get_products(product_data)

    stockchecker.add_prices_to_products(products, prices)

    website_list = stockchecker.create_website_list()

    stockchecker.distribute_products(website_list, products)

    stockchecker.run(website_list)

    scraped_products: list[ScrapedProduct] = []
    for website in website_list:
        scraped_products.extend(website.scraped_products)

    print(f"Scraped products: {len(scraped_products)}")


if __name__ == "__main__":
    main()
