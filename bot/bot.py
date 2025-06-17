import telebot
import requests
from aiogram.dispatcher.middlewares import data

bot = telebot.TeleBot('API')
api_key = 'API(openweather)'
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет, как всегда вовремя, напиши название города')
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city_name = message.text.strip().lower()
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    )
    if response.status_code == 200:
     data = response.json()
     temp = data['main']['temp']

     bot.send_message(message.chat.id, f'Сейчас погода:\nТемпература: {temp}°C')
     image = 'sunny.png' if temp > 5.0 else 'sun.png'
     file = open('./' + image, 'rb')
     bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'Город не найден!')


bot.polling()
