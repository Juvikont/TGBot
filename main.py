from telegram import Bot, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import time

from service.config import API_TOKEN
from apis.bittrex import BittrexClient
from apis.bittrex import BittrexError

CALLBACK_BUTTON1_LEFT = 'callback_button1_left'
CALLBACK_BUTTON2_RIGHT = 'callback_button2_right'
CALLBACK_BUTTON3_MORE = 'callback_button3_more'
CALLBACK_BUTTON4_BACK = 'callback_button4_back'
CALLBACK_BUTTON5_TIME = 'callback_button5_time'
CALLBACK_BUTTON6_PRICE = 'callback_button6_price'
CALLBACK_BUTTON7_PRICE = 'callback_button7_price'
CALLBACK_BUTTON8_PRICE = 'callback_button8_price'
CALLBACK_BUTTON_HIDE_KEYBOARD = "callback_button9_hide"

TITLES = {
    CALLBACK_BUTTON1_LEFT: 'Новое сообщение ',
    CALLBACK_BUTTON2_RIGHT: 'Отредактировать',
    CALLBACK_BUTTON3_MORE: 'Ещё',
    CALLBACK_BUTTON4_BACK: 'Назад',
    CALLBACK_BUTTON5_TIME: 'Время',
    CALLBACK_BUTTON6_PRICE: 'BTC',
    CALLBACK_BUTTON7_PRICE: 'LTC',
    CALLBACK_BUTTON8_PRICE: 'ETH',
    CALLBACK_BUTTON_HIDE_KEYBOARD: "Спрять клавиатуру",
}

REPLY_BUTTON1_RIGHT = 'reply_button1_right'

TITLES_REP = {
    REPLY_BUTTON1_RIGHT: 'Правая кнопка',
}

client = BittrexClient()


def reply_keyboard():
    menu_keyboard = [['', 'Выберите пол'],
                     ['Мужской', 'Женский']]

    return ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=False)


def base_inline_keyboard():
    # Основная клавиатура
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON_HIDE_KEYBOARD)
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def base_inline_keyboard2():
    # Дополнительная клавиатура. Доступна только и основной
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME)
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ]

    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(bot: Bot, update: Update, context=CallbackContext):
    query = update.callback_query
    data = query.data
    now = time.ctime()

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON1_LEFT:
        # Текст остается клава пропадает, текст прежний
        query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,

        )
        context.bot.send_message(
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
            reply_markup=base_inline_keyboard2(),
        )
    elif data == CALLBACK_BUTTON_HIDE_KEYBOARD:
        # Спрятать клавиатуру
        context.bot.send_message(
            chat_id=chat_id,
            text="Спрятали клавиатуру\n\nНажмите /start чтобы вернуть её обратно",
            reply_markup=ReplyKeyboardRemove(),
        )


def start(bot: Bot, update: Update, context=CallbackContext):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Вас приветствует Merchebot!',
        reply_markup=base_inline_keyboard(),
    )


def help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Это учебный бот \n\n'
             'Список доступных команд надится в меню\n\n'
             'Так же я отвечу на любое сообщение',
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


def sticker_info(bot: Bot, update: Update, context=CallbackContext):
    sticker = update.message.sticker.file_id
    emoji = update.message.sticker.emoji
    text = 'Ваш стикер ID:\n\n{}\n\nEmoji вашего стикера:\n{}'.format(sticker, emoji)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=base_inline_keyboard(),
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
    message_handler = MessageHandler(Filters.text, echo)
    button_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
    menu_handler = CallbackQueryHandler(callback=reply_keyboard)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(sticker_handler)
    updater.dispatcher.add_handler(button_handler)
    updater.dispatcher.add_handler(menu_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
