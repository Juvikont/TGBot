import uuid

from yandex_checkout import Configuration, Payment


# Configuration.account_id = <Идентификатор магазина>
# Configuration.secret_key = <Секретный ключ>


def createyandexpayment(price, currency):
    print('You are here'+str(uuid.uuid4()))
    # payment = Payment.create({
    #     "amount": {
    #         "value": price,
    #         "currency": currency
    #     },
    #     "confirmation": {
    #         "type": "redirect",
    #         "return_url": None
    #     },
    #     "capture": True,
    #     "description": "Заказ №1"
    # }, uuid.uuid4())
    # print(payment)
    # return payment
