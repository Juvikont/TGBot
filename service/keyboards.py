from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

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

TITLES = {
    CALLBACK_BUTTON1_LEFT: 'Новое сообщение ',
    CALLBACK_BUTTON2_RIGHT: 'Отредактировать',
    CALLBACK_BUTTON3_MORE: 'Ещё',
    CALLBACK_BUTTON4_BACK: 'Назад',
    CALLBACK_BUTTON5_TIME: 'Время',
    CALLBACK_BUTTON6_PRICE: 'BTC',
    CALLBACK_BUTTON7_PRICE: 'LTC',
    CALLBACK_BUTTON8_PRICE: 'ETH',
    CALLBACK_BUTTON9_HIDE_KEYBOARD: "Спрять клавиатуру",
    CALLBACK_BUTTON10_TSHIRTS: 'Майки',
    CALLBACK_BUTTON11_JEANS: 'Джинсы',
    CALLBACK_BUTTON12_BOOTS: 'Обувь',
    CALLBACK_BUTTON13_JACKETS: 'Куртки',
    CALLBACK_BUTTON14_BUY: 'Купить',
    CALLBACK_BUTTON15_MORE_PHOTOS: 'Подробнее'
}

REPLY_BUTTON1_STORE = '\U0001F6D2 Магазин'
REPLY_BUTTON1_CURRENCY = '\U0001F4B0 Курсы валют'


def reply_keyboard():
    # основная клавиатура(снизу)- меню выбора
    menu_keyboard = [
        [
            KeyboardButton(text=REPLY_BUTTON1_STORE),
            KeyboardButton(text=REPLY_BUTTON1_CURRENCY),
        ],

    ]

    return ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True)


def purchase_inline_keyboard():
    # Дополнительная inline клавиатура- покупка товара. Доступна только из shop_inline_keyboard
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON14_BUY], callback_data=CALLBACK_BUTTON14_BUY),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON15_MORE_PHOTOS], callback_data=CALLBACK_BUTTON15_MORE_PHOTOS),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def currency_inline_keyboard():
    # Дополнительная inline клавиатура- курсы валют. Доступна только из reply_keyboard
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE, ),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
        ],

    ]
    return InlineKeyboardMarkup(keyboard)


def shop_inline_keyboard():
    # Дополнительная inline клавиатура- категории товаров
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON10_TSHIRTS], callback_data=CALLBACK_BUTTON10_TSHIRTS),
        ],
        [InlineKeyboardButton(TITLES[CALLBACK_BUTTON11_JEANS], callback_data=CALLBACK_BUTTON11_JEANS)
         ],
        [InlineKeyboardButton(TITLES[CALLBACK_BUTTON12_BOOTS], callback_data=CALLBACK_BUTTON12_BOOTS),
         ],
        [InlineKeyboardButton(TITLES[CALLBACK_BUTTON13_JACKETS], callback_data=CALLBACK_BUTTON13_JACKETS)
         ]
    ]
    return InlineKeyboardMarkup(keyboard, row_width=1)


def base_inline_keyboard():
    # Основная клавиатура
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON9_HIDE_KEYBOARD)
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
