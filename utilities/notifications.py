
from os import environ

import pyperclip
from models.scrapedproduct import ScrapedProduct
from persistence.database import session
from pywhatkit.whats import sendwhatmsg_to_group_instantly


def send_notif(product: ScrapedProduct, group_id: str) -> None:
    p = product
    msg = f"{p.url}\nPrice: {p.item_price}"
    pyperclip.copy(msg)
    sendwhatmsg_to_group_instantly(
        group_id=group_id, message="\v", wait_time=7, tab_close=True, close_time=1)


def send_notifications() -> None:
    if environ.get("notifs") != "True":
        return
    whatsapp_group_id = environ.get("WHATSAPP_GROUP_ID")

    if not isinstance(whatsapp_group_id, str):
        environ["notifs"] == "False"
        print("No WhatsApp group id specified")
        return

    products: list[ScrapedProduct] = session.query(ScrapedProduct).all()
    for p in products:
        send_notif(p, whatsapp_group_id)
