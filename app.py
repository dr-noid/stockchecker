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

    all_scraped_products: list[ScrapedProduct] = []
    for website in website_list:
        all_scraped_products.extend(website.scraped_products)

    print(f"Scraped products: {len(all_scraped_products)}")

    filter_availability(all_scraped_products)

    print(f"Filtered products len: {len(all_scraped_products)}")


def filter_availability(products: list[ScrapedProduct]):
    for product in products:
        if not product.availability:
            products.remove(product)


def filter_price(products: list[ScrapedProduct], prices: dict[int, int]):
    for product in products:
        # TODO: match scrapedproduct and prices with id's


if __name__ == "__main__":
    main()
