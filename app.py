import stockchecker
from models.scrapedproduct import ScrapedProduct
from persistence import database
from utilities import args, json_parser


def main():
    args.parse_args()

    database.add_metadata(ScrapedProduct)

    prices = json_parser.get_prices("prices.json")
    products = json_parser.get_products("products.json")

    stockchecker.add_prices_to_products(products, prices)

    website_list = stockchecker.create_website_list()

    stockchecker.distribute_products(website_list, products)

    print("running now")
    stockchecker.run(website_list)

    scraped_products: list[ScrapedProduct] = []
    for website in website_list:
        scraped_products.extend(website.scraped_products)

    print(f"Amount of scraped products: {len(scraped_products)}")

    for scraped_product in scraped_products:
        database.save(scraped_product)


if __name__ == "__main__":
    main()
