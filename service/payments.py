import uuid

from yandex_checkout import Configuration, Payment

from repository.product_repository import Product
from service.product_services import Product_Services


# Configuration.account_id = <Идентификатор магазина>
# Configuration.secret_key = <Секретный ключ>


def createyandexpayment():
    payment = Payment.create({
        "amount": {
            "value": Product.product_price,
            "currency": "USD"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": None
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())
