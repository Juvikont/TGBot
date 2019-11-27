from service.config import API_TOKEN
import telebot
from telebot import types
from service import productservices as products

bot = telebot.TeleBot(API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_products = types.KeyboardButton('Наши товары', request_location=False)
btn_cart = types.KeyboardButton('Корзина')
btn_delivery = types.KeyboardButton('Способы доставки')
markup_menu.add(btn_products, btn_cart, btn_delivery)

product_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_tshirts = types.KeyboardButton('Майки')
btn_jeans = types.KeyboardButton('Джинсы')
btn_boots = types.KeyboardButton('Обувь')
btn_jackets = types.KeyboardButton('Куртки')
btn_back = types.KeyboardButton('Назад')
product_menu.add(btn_boots, btn_jackets, btn_jeans, btn_tshirts, btn_back)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, 'Вас приветствует Merchebot! ', reply_markup=markup_menu)


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text.lower() == 'привет':
        bot.send_sticker(message.chat.id, 'CAADAgADCQADuDxkCAJGmwpNLbuoFgQ')
    elif message.text.lower() == 'пока':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

    elif message.text.lower() == 'наши товары':
        bot.send_message(message.chat.id, 'Наши товары', reply_markup=product_menu)
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, 'Вас приветствует Merchebot! ', reply_markup=markup_menu)
    elif message.text.lower() == 'обувь':
        bot.send_photo(message.chat.id,products.get_product_by_id)
    else:
        bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['sticker'])
def sticker_info(message):
    print(message.sticker.file_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
