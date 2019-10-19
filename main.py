import locale
import time
import io
from PIL import Image

from telegram import Bot, ReplyKeyboardRemove
from telegram import Update, ParseMode, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

from apis.bittrex import BittrexClient
from apis.bittrex import BittrexError
from service.config import API_TOKEN
from service.keyboards import base_inline_keyboard2, base_inline_keyboard, reply_keyboard, currency_inline_keyboard, \
    shop_inline_keyboard, purchase_inline_keyboard, TITLES

from service.product_services import Product_Services

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

REPLY_BUTTON1_STORE = '\U0001F6D2 Магазин'
REPLY_BUTTON1_CURRENCY = '\U0001F4B0 Курсы валют'

client = BittrexClient()
locale.setlocale(locale.LC_ALL, "ru")


def keyboard_callback_handler(bot: Bot, update: Update, context=CallbackContext):
    query = update.callback_query
    data = query.data
    print(data)
    now = time.ctime()

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text
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

        for product in Product_Services.getproducts():
            x = product.photos
            result = None
            for i in x:
                if i.is_main:
                    result = i
            print(result)
            image = Image.open(result.photo_name + result.photo_ext)
            photo = io.BytesIO(result.photo_content)
            photo.name = result.photo_name
            image.save(photo, 'JPG')
            photo.seek(0)
            print(photo)
            text = '{}\n{}$'.format(product.product_name, product.product_price)
            bot.send_photo(
                chat_id=chat_id,
                photo_content=InputFile(result.photo_content),
                caption=text,
                reply_markup=purchase_inline_keyboard()
            )
        return


def reply_handler(bot: Bot, update: Update):
    current_text = update.message.text
    text = time.strftime("%d %b %Y %H:%M")
    if current_text == REPLY_BUTTON1_CURRENCY:
        text = 'Актуальные {}\n\n на {}'.format(REPLY_BUTTON1_CURRENCY, text)
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
             'Список доступных команд надится в меню\n\n'
             'Так же я отвечу на любое сообщение',
        reply_markup=base_inline_keyboard(),
    )


def sticker_info(bot: Bot, update: Update, context=CallbackContext):
    sticker = update.message.sticker.file_id
    emoji = update.message.sticker.emoji
    text = 'Ваш стикер ID:\n\n{}\n\nEmoji вашего стикера:\n{}'.format(sticker, emoji)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=base_inline_keyboard(),
    )


def show_time(bot: Bot, update: Update):
    text = time.ctime()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=base_inline_keyboard()
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

    )

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    time_handler = CommandHandler('time', show_time)
    sticker_handler = MessageHandler(Filters.sticker, sticker_info)
    button_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
    currency_handler = MessageHandler(Filters.text, reply_handler)
    message_handler = MessageHandler(Filters.text, echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(sticker_handler)
    updater.dispatcher.add_handler(button_handler)
    updater.dispatcher.add_handler(currency_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
