from telebot import types

def lang_button():
    kybd = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Русский')
    but2 = types.KeyboardButton('English')
    kybd.add(but1, but2)
    return kybd

def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Отправить номер телефона📞', request_contact=True)
    kb.add(but)
    return kb

def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Отправить локацию🌐', request_location=True)
    kb.add(but)
    return kb
