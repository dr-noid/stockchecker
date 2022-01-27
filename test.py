import app
import stockchecker
from models.product import Product
from sites.alternate import Alternate
from utilities import json_parser

alternate = Alternate()

products = [Product(product_id=2,
                    url="https://www.alternate.nl/Grafische-kaarten/RTX-3070")]

price_data = json_parser.parse_json_file("prices.json")

prices = json_parser.get_prices(price_data)

stockchecker.add_prices_to_products(products, prices)

alternate.products.append(products[0])

alternate.run()

items = alternate.scraped_products

print(items)
