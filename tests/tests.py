from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging
from telebot import types
from service.config import API_TOKEN as token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_products = types.KeyboardButton('Наши товары', request_location=True)
btn_cart = types.KeyboardButton('Корзина')
btn_delivery = types.KeyboardButton('Способы доставки')
markup_menu.to_json()
markup_menu.add(btn_products, btn_cart, btn_delivery)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!",
                             reply_markup=markup_menu)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text, reply_markup=markup_menu)


echo_handler = MessageHandler(Filters.all, echo)
dispatcher.add_handler(echo_handler)

def caps(update, context):
    text_caps = ' '.join(context).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=" Извините, я не понял эту команду. ")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
updater.start_polling()

def remade_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


tshirt = Product(
    product_name='Calvin Kleine',
    product_description='Geniune silk',
    product_price=65,
    product_quantity=1,
    product_type='Tshirt',
    product_sex='Male')

add_product(tshirt)

