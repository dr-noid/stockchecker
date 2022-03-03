
from os import environ

from models.scrapedproduct import ScrapedProduct
from persistence.database import session
from pywhatkit.whats import sendwhatmsg_to_group_instantly

from utilities import args_parser


def send_notif(product: ScrapedProduct, group_id: str) -> None:
    p = product
    msg = f"{p.url}\nPrice: {p.item_price}"
    sendwhatmsg_to_group_instantly(
        group_id=group_id, message=msg, wait_time=7, tab_close=True, close_time=0)


def send_notifications() -> None:
    whatsapp_group_id = environ.get("WHATSAPP_GROUP_ID")

    if not isinstance(whatsapp_group_id, str):
        environ["notifs"] == "False"
        print("No WhatsApp group id specified")
        return

    products: list[ScrapedProduct] = session.query(ScrapedProduct).all()
    print(len(products))
    for p in products:
        print(p)
        send_notif(p, whatsapp_group_id)
