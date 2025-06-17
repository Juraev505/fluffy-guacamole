import telebot
import buttons
import database

bot = telebot.TeleBot('API')
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users[user_id] = {}


    bot.send_message(user_id, "🌍 Выберите язык / Choose your language:", reply_markup=buttons.lang_button())
    bot.register_next_step_handler_by_chat_id(user_id, set_language)

def set_language(message):
    user_id = message.from_user.id
    lang = message.text

    if lang == 'Русский':
        users[user_id]['lang'] = 'ru'
        bot.send_message(user_id, 'Приветствую 🫡, давай начнем регистрацию. Введи свое имя:',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif lang == 'English':
        users[user_id]['lang'] = 'en'
        bot.send_message(user_id, 'Welcome 🫡, let\'s start registration. Enter your name:',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Пожалуйста, выберите язык с кнопки / Please select a language from the keyboard.')
        return

    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    users[user_id]['name'] = user_name

    lang = users[user_id].get('lang', 'ru')
    if lang == 'ru':
        bot.send_message(user_id, 'Отлично! Теперь свой номер телефона!',
                         reply_markup=buttons.num_button())
    else:
        bot.send_message(user_id, 'Great! Now send your phone number!',
                         reply_markup=buttons.num_button())

    bot.register_next_step_handler(message, get_num)

def get_num(message):
    user_id = message.from_user.id
    lang = users[user_id].get('lang', 'ru')

    if message.contact:
        user_num = message.contact.phone_number
        users[user_id]['number'] = user_num

        if lang == 'ru':
            bot.send_message(user_id, 'Отлично, теперь отправь локацию!',
                             reply_markup=buttons.loc_button())
        else:
            bot.send_message(user_id, 'Great, now send your location!',
                             reply_markup=buttons.loc_button())

        bot.register_next_step_handler(message, get_loc)
    else:
        if lang == 'ru':
            bot.send_message(user_id, 'Пожалуйста, отправьте номер через кнопку!')
        else:
            bot.send_message(user_id, 'Please send your number using the button!')
        bot.register_next_step_handler(message, get_num)

def get_loc(message):
    user_id = message.from_user.id
    lang = users[user_id].get('lang', 'ru')

    if message.location:
        user_loc = message.location
        if 'name' in users[user_id] and 'number' in users[user_id]:
            name = users[user_id]['name']
            number = users[user_id]['number']
            database.register(user_id, name, number, str(user_loc))

            if lang == 'ru':
                bot.send_message(user_id, 'Регистрация прошла успешно!',
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(user_id, 'Registration completed successfully!',
                                 reply_markup=telebot.types.ReplyKeyboardRemove())

            del users[user_id]
        else:
            bot.send_message(user_id, 'Ошибка: отсутствуют данные. Попробуйте /start сначала.')
    else:
        if lang == 'ru':
            bot.send_message(user_id, 'Пожалуйста, отправьте локацию через кнопку!')
        else:
            bot.send_message(user_id, 'Please send your location using the button!')
        bot.register_next_step_handler(message, get_loc)

bot.polling()






