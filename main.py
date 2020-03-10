import locale
import time
import uuid
from enum import Enum

from telegram import Bot, ReplyKeyboardRemove
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

from apis.bittrex import BittrexClient
from apis.bittrex import BittrexError
from repository.payment_repository import Payment, add_payment, get_payment_by_customer, get_payment_by_payment_id
from service.config import API_TOKEN
from service.keyboards import base_inline_keyboard2, base_inline_keyboard, reply_keyboard, currency_inline_keyboard, \
    shop_inline_keyboard, purchase_inline_keyboard, check_inline_keyboard
from service.payments import createyandexpayment

from service.productservices import ProductServices

CALLBACK_BUTTON1_LEFT = 'callback_button1_left'
CALLBACK_BUTTON2_RIGHT = 'callback_button2_right'
CALLBACK_BUTTON3_MORE = 'callback_button3_more'
CALLBACK_BUTTON4_BACK = 'callback_button4_back'
CALLBACK_BUTTON5_TIME = 'callback_button5_time'
CALLBACK_BUTTON6_PRICE = 'callback_button6_price'
CALLBACK_BUTTON7_PRICE = 'callback_button7_price'
CALLBACK_BUTTON8_PRICE = 'callback_button8_price'
CALLBACK_BUTTON9_HIDE_KEYBOARD = "callback_button9_hide"
CALLBACK_BUTTON10_TSHIRTS = 'callback_button10_tshirts'
CALLBACK_BUTTON11_JEANS = 'callback_button11_jeans'
CALLBACK_BUTTON12_BOOTS = 'callback_button12_boots'
CALLBACK_BUTTON13_JACKETS = 'callback_button13_jackets'
CALLBACK_BUTTON14_BUY = 'callback_button14_buy'
CALLBACK_BUTTON15_MORE_PHOTOS = 'callback_button15_more_photos'
CALLBACK_BUTTON16_BACK_SHOP = 'callback_button16_back_shop'
CALLBACK_BUTTON17_CHECK = 'callback_button17_check'

REPLY_BUTTON1_STORE = '\U0001F6D2 Магазин'
REPLY_BUTTON2_CURRENCY = '\U0001F4B0 Курсы валют'
REPLY_BUTTON3_PAYMENTS = '\U0001F9FE Мои оплаты'

client = BittrexClient()
locale.setlocale(locale.LC_ALL, "ru")


class ProductTypes(Enum):
    tshirts = 'T-Shirt'
    boots = 'Boots'
    jeans = 'Jeans'
    jackets = 'Jacket'


def find_product_main_photo(photos):
    # функия пл поиску фото
    for photo in photos:
        if photo.is_main:
            return photo


def find_product_id(text):
    product_id = int(text.split("\n")[0].split(':')[1].strip())
    return product_id


def sort_by_main(photo):
    return photo.is_main


def keyboard_callback_handler(bot: Bot, update: Update, context=CallbackContext):
    query = update.callback_query
    data = query.data
    now = time.ctime()

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text
    info = update.effective_message
    print(info)
    print(chat_id)

    if data == CALLBACK_BUTTON1_LEFT:
        # Текст остается клава пропадает, текст прежний
        query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,

        )
        bot.send_message(
            chat_id=chat_id,
            text='Новое сообщение\n\ncallback_query_data={}'.format(data),
            reply_markup=base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON2_RIGHT:
        # Редактирование сообщения, текст остается
        query.edit_message_text(
            text='Успешно отредактировано в {}'.format(now),
            reply_markup=base_inline_keyboard(),
        )
        return
    elif data == CALLBACK_BUTTON3_MORE:
        # Показать след экран клавы(текст тот же, другой массив кнопок)
        query.edit_message_text(
            text=current_text,
            reply_markup=base_inline_keyboard2(),
        )
    elif data == CALLBACK_BUTTON4_BACK:
        # показать предыдущий экран клавы(текст тот же, другой массив кнопок)
        query.edit_message_text(
            text=current_text,
            reply_markup=base_inline_keyboard(),
        )

    elif data == CALLBACK_BUTTON5_TIME:
        text = "*Точное время*\n\n{}".format(now)
        query.edit_message_text(
            text=text,
            pars_mode=ParseMode.MARKDOWN,
            reply_markup=base_inline_keyboard2(),
        )
    elif data in (CALLBACK_BUTTON6_PRICE, CALLBACK_BUTTON7_PRICE, CALLBACK_BUTTON8_PRICE):
        pair = {
            CALLBACK_BUTTON6_PRICE: "USD-BTC",
            CALLBACK_BUTTON7_PRICE: "USD-LTC",
            CALLBACK_BUTTON8_PRICE: "USD-ETH",
        }[data]

        try:
            current_price = client.get_last_price(pair=pair)
            text = "*Курс валюты:*\n\n*{}* = {}$".format(pair, current_price)
        except BittrexError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=currency_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON9_HIDE_KEYBOARD:
        # Спрятать клавиатуру
        bot.send_message(
            chat_id=chat_id,
            text="Спрятали клавиатуру\n\nНажмите /start чтобы вернуть её обратно",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif data == CALLBACK_BUTTON10_TSHIRTS:

        for product in ProductServices.getproductbytype(ProductTypes.tshirts.value):
            x = product.photos
            result = list(filter(lambda p: p.is_main, x))[0]
            # result= find_product_main_photo(x)
            try:
                current_price_btc = int(product.product_price) / int(client.get_last_price(pair="USD-BTC"))
                current_price_ltc = int(product.product_price) / int(client.get_last_price(pair="USD-LTC"))
                current_price_eth = int(product.product_price) / int(client.get_last_price(pair="USD-ETH"))
                text = 'Каталоговый номер: {}\nНазвание: {}\nЦена: {}$\n Цена BTC: \n{}'.format(product.id,
                                                                                                product.product_name,
                                                                                                product.product_price,
                                                                                                current_price_btc)
            except BittrexError:
                text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
            bot.send_photo(
                chat_id=chat_id,
                photo=open('static/' + result.photo_name + result.photo_ext, 'rb'),
                caption=text,
                reply_markup=purchase_inline_keyboard()

            )
        return
    elif data == CALLBACK_BUTTON11_JEANS:

        for product in ProductServices.getproductbytype(ProductTypes.jeans.value):
            x = product.photos
            result = list(filter(lambda p: p.is_main, x))[0]
            # result= find_product_main_photo(x)
            try:
                current_price_btc = int(product.product_price) / int(client.get_last_price(pair="USD-BTC"))
                current_price_ltc = int(product.product_price) / int(client.get_last_price(pair="USD-LTC"))
                current_price_eth = int(product.product_price) / int(client.get_last_price(pair="USD-ETH"))
                text = 'Каталоговый номер: {}\nНазвание: {}\nЦена: {}$\n Цена BTC: \n{}'.format(product.id,
                                                                                                product.product_name,
                                                                                                product.product_price,
                                                                                                current_price_btc)
            except BittrexError:
                text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
            bot.send_photo(
                chat_id=chat_id,
                photo=open('static/' + result.photo_name + result.photo_ext, 'rb'),
                caption=text,
                reply_markup=purchase_inline_keyboard()

            )
        return
    elif data == CALLBACK_BUTTON12_BOOTS:

        for product in ProductServices.getproductbytype(ProductTypes.boots.value):
            x = product.photos
            result = list(filter(lambda p: p.is_main, x))[0]
            # result= find_product_main_photo(x)
            try:
                current_price_btc = int(product.product_price) / int(client.get_last_price(pair="USD-BTC"))
                current_price_ltc = int(product.product_price) / int(client.get_last_price(pair="USD-LTC"))
                current_price_eth = int(product.product_price) / int(client.get_last_price(pair="USD-ETH"))
                text = 'Каталоговый номер: {}\nНазвание: {}\nЦена: {}$\n Цена BTC: \n{}'.format(product.id,
                                                                                                product.product_name,
                                                                                                product.product_price,
                                                                                                current_price_btc)
            except BittrexError:
                text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
            bot.send_photo(
                chat_id=chat_id,
                photo=open('static/' + result.photo_name + result.photo_ext, 'rb'),
                caption=text,
                reply_markup=purchase_inline_keyboard()

            )
        return
    elif data == CALLBACK_BUTTON13_JACKETS:

        for product in ProductServices.getproductbytype(ProductTypes.jackets.value):
            x = product.photos
            result = list(filter(lambda p: p.is_main, x))[0]
            # result= find_product_main_photo(x)
            try:
                current_price_btc = int(product.product_price) / int(client.get_last_price(pair="USD-BTC"))
                current_price_ltc = int(product.product_price) / int(client.get_last_price(pair="USD-LTC"))
                current_price_eth = int(product.product_price) / int(client.get_last_price(pair="USD-ETH"))
                text = 'Каталоговый номер: {}\nНазвание: {}\nЦена: {}$\n Цена BTC:\n {}'.format(product.id,
                                                                                                product.product_name,
                                                                                                product.product_price,
                                                                                                current_price_btc)
            except BittrexError:
                text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
            bot.send_photo(
                chat_id=chat_id,
                photo=open('static/' + result.photo_name + result.photo_ext, 'rb'),
                caption=text,
                reply_markup=purchase_inline_keyboard()

            )
        return
    elif data == CALLBACK_BUTTON16_BACK_SHOP:
        # показать категории магазина(доступен только из продуктов)
        text = 'Ниже предствлены товары данного магазина. Нажмите чтобы выбрать соответствующую категорию.'
        bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=shop_inline_keyboard()

        )
        return
    elif data == CALLBACK_BUTTON15_MORE_PHOTOS:
        product = ProductServices.getproductbyid(find_product_id(update.effective_message.caption))
        for photo in sorted(product.photos, key=sort_by_main):
            if photo.is_main:
                try:
                    current_price_btc = int(product.product_price) / int(client.get_last_price(pair="USD-BTC"))
                    current_price_ltc = int(product.product_price) / int(client.get_last_price(pair="USD-LTC"))
                    current_price_eth = int(product.product_price) / int(client.get_last_price(pair="USD-ETH"))
                    text = 'Каталоговый номер: {}\nНазвание: {}\nЦена: {}$\n Цена BTC:\n {}'.format(product.id,
                                                                                                    product.product_name,
                                                                                                    product.product_price,
                                                                                                    current_price_btc)
                except BittrexError:
                    text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
                bot.send_photo(
                    chat_id=chat_id,
                    photo=open('static/' + photo.photo_name + photo.photo_ext, 'rb'),
                    caption=text,
                    reply_markup=purchase_inline_keyboard()
                )
            else:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=open('static/' + photo.photo_name + photo.photo_ext, 'rb'),
                )

    elif data == CALLBACK_BUTTON14_BUY:
        product = ProductServices.getproductbyid(find_product_id(update.effective_message.caption))
        createyandexpayment(product.product_price, 'USD')
        payment = Payment(str(uuid.uuid4()), 'pending', product.product_price, 'USD', str(uuid.uuid4()),
                          str(time.ctime()), product.id, chat_id)
        add_payment(payment)
        # Отправить URL API Yandex для оплаты клиенту
        bot.send_message(
            chat_id=chat_id,
            text='https://checkout.yandex.com/developers/payments/quick-start'
        )
    elif data == CALLBACK_BUTTON17_CHECK:
        text = current_text
        payment = get_payment_by_payment_id(int(text.split("\n")[0].split(':')[1].strip()))
        if payment.payment_status == 'succeed':
            bot.send_message(
                chat_id=chat_id,
                text='Ваш платеж подтвержден. Ожидайте доставки'
            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text='Ожидаем оплаты',
            )


def reply_handler(bot: Bot, update: Update):
    current_text = update.message.text
    text = time.strftime("%d %b %Y %H:%M")
    if current_text == REPLY_BUTTON2_CURRENCY:
        text = 'Актуальные {}\n\n на {}'.format(REPLY_BUTTON2_CURRENCY, text)
        bot.send_message(
            text=text,
            chat_id=update.message.chat_id,
            reply_markup=currency_inline_keyboard()
        )
    elif current_text == REPLY_BUTTON1_STORE:
        text = 'Ниже предствлены товары данного магазина. Нажмите чтобы выбрать соответствующую категорию.'
        bot.send_message(
            text=text,
            chat_id=update.message.chat_id,
            reply_markup=shop_inline_keyboard()
        )
    elif current_text == REPLY_BUTTON3_PAYMENTS:
        chat_id = update.message.chat_id
        for payment in get_payment_by_customer(chat_id):
            text = 'Номер платежа: {}\nТовар: {}\nСтатус: {}\nДата оплаты: {} '.format(payment.payment_id,
                                                                                       payment.product.product_name,
                                                                                       payment.payment_status,
                                                                                       payment.payment_date)
            print(text)
            bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=check_inline_keyboard()
            )


def start(bot: Bot, update: Update, context=CallbackContext):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Вас приветствует Merchebot!',
        reply_markup=reply_keyboard(),
    )


def help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Это учебный бот \n\n'
             'Список доступных команд надится в меню\n\n',
        reply_markup=reply_keyboard(),
    )


def sticker_info(bot: Bot, update: Update, context=CallbackContext):
    sticker = update.message.sticker.file_id
    emoji = update.message.sticker.emoji
    text = 'Ваш стикер ID:\n\n{}\n\nEmoji вашего стикера:\n{}'.format(sticker, emoji)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=reply_keyboard(),
    )


def show_time(bot: Bot, update: Update):
    text = time.ctime()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=reply_keyboard()
    )


def echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = 'Ваш ID = {}\n\n{}'.format(chat_id, update.message.text)
    bot.send_message(
        text=text,
        chat_id=update.message.chat_id,
        reply_markup=reply_keyboard()
    )


def main():
    bot = Bot(
        token=API_TOKEN,
    )
    updater = Updater(
        bot=bot,
        # use_context=True,

    )

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    time_handler = CommandHandler('time', show_time)
    sticker_handler = MessageHandler(Filters.sticker, sticker_info)
    button_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
    keyboard_handler = MessageHandler(Filters.text, reply_handler)
    message_handler = MessageHandler(Filters.text, echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(sticker_handler)
    updater.dispatcher.add_handler(button_handler)
    updater.dispatcher.add_handler(keyboard_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
