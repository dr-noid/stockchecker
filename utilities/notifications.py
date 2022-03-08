import pyperclip
from models.scrapedproduct import ScrapedProduct
from persistence import database
from pywhatkit import whats

from utilities.settings import program_settings


def run() -> None:
    if not program_settings.notifications:
        return
    products = database.session.query(ScrapedProduct).all()
    for product in products:
        notify(product)


def notify(scraped_product: ScrapedProduct) -> None:
    msg = f"url: {scraped_product.url}\nid/gpu: {scraped_product.product_id}\nprice: {scraped_product.item_price}"
    print(msg)
    pyperclip.copy(msg)
    whats.sendwhatmsg_to_group_instantly(
        group_id=program_settings.whatsapp_group_id, message="\v", wait_time=7, tab_close=True, close_time=1)


if __name__ == '__main__':
    pass
