import app
from models.product import Product
from sites.alternate import Alternate

alternate = Alternate()

product = Product(product_id=1,
                  url="https://www.alternate.nl/Grafische-kaarten/RTX-3070")

alternate.products.append(product)

alternate.run()

items = alternate.scraped_products

print(len(items))

app.filter_availability(items)

print(len(items))
