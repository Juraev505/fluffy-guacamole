


import telebot
from WOrk import buttons

bot = telebot.TeleBot('7996561395:AAGHWOuW7_kheUomnlGBvOVZr9Xvx3036Iw')
user_data = {}

def get_exchange_rates():
    import requests
    URL = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
    data = requests.get(URL).json()
    rates = {'UZS': 1.0}
    for item in data:

        currency_code = item['Ccy']
        try:
            rate = float(item['Rate'])
            rates[currency_code] = rate
        except (ValueError, KeyError):
            pass

    return rates
@bot.message_handler(commands=['start'])

def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Привет! Я твой личный конвертер валют , Отпрваь мне что угодно и я угадаю твое имя🧙‍♂️', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, choose_currency)

@bot.message_handler(commands=['Text'])
def choose_currency(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or message.from_user.username or "друг"

    kb = buttons.num_button()
    if message.text not in ['USD', 'EUR', 'JPY', 'GBP', 'UZS', 'RUB']:
        bot.send_message(user_id, f'Выбери любую валюту которую будем обменивать, {user_name}!', reply_markup=kb)
        bot.register_next_step_handler(message, choose_currency)
        return


    user_data[user_id] = {'from': message.text}  # сохраняем выбранную валюту
    bot.send_message(user_id, f'Теперь выбери валюту, на которую будем обменивать:', reply_markup=kb)
    bot.register_next_step_handler(message, currency_to)

def currency_to(message):
    user_id = message.from_user.id
    if message.text not in ['USD', 'EUR', 'JPY', 'GBP', 'UZS', 'RUB']:
        bot.send_message(user_id, 'Пожалуйста, выбери валюту кнопками.')
        bot.register_next_step_handler(message, currency_to)
        return

    user_data[user_id]['to'] = message.text  # сохраняем валюту для конвертации
    bot.send_message(user_id, 'Сколько нужно обменять? Введи сумму:',reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, amount_entered)  # Переходим к вводу суммы

def amount_entered(message):
    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введи число.')
        return
    user_data[message.chat.id]['amount'] = amount
    from_currency = user_data[message.chat.id]['from']
    to_currency = user_data[message.chat.id]['to']
    rates = get_exchange_rates()
    if from_currency not in rates or to_currency not in rates:
        bot.send_message(message.chat.id, "Ошибка: валюта не поддерживается.")
        return

    result = amount * rates[from_currency] / rates[to_currency]
    bot.send_message(message.chat.id, f"{amount} {from_currency} = {result:.4f} {to_currency}")

    bot.send_message(message.chat.id, 'Если хочешь сделать еще один обмен, выбери валюту:')
    kb = buttons.num_button()
    bot.send_message(message.chat.id, 'Выбери валюту:', reply_markup=kb)
    bot.register_next_step_handler(message, choose_currency)


bot.polling()
