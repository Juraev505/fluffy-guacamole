from telebot import types


def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('USD')
    but2 = types.KeyboardButton('EUR')
    but3 = types.KeyboardButton('JPY')
    but4 = types.KeyboardButton('GBP')
    but5 = types.KeyboardButton('UZS')
    but6 = types.KeyboardButton('RUB')

    kb.add(but1, but2)
    kb.add(but3, but4)
    kb.add(but5, but6)
    return kb
