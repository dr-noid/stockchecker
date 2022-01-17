import app
import stockchecker
from models.product import Product
from sites.alternate import Alternate
from utilities import json_parser

alternate = Alternate()

product = Product(product_id=2,
                  url="https://www.alternate.nl/Grafische-kaarten/RTX-3070")

alternate.products.append(product)

alternate.run()

price_data = json_parser.parse_json_file("prices.json")

prices = json_parser.get_prices(price_data)

items = alternate.scraped_products

print(len(items))

app.filter_availability(items)

print(len(items))

app.filter_price(items, prices)

print(len(items))
