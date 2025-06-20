import telebot
import database
import buttons
import json



# Создаем объект бота
bot = telebot.TeleBot('7315235690:AAEevKLuBlJ_XJChtEutBpL2Jlit5pcUQ9Y')
# Создаем хранилище временных данных
users = {}
admins = {}
admin_id = 211029038
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if database.check_user(user_id):
        products = database.get_pr_buttons()
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(products))
    else:
        bot.send_message(user_id, 'Приветствую! Давайте начнем регистрацию, '
                                  'введите свое имя!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text

    bot.send_message(user_id, 'Отлично! Теперь свой номер телефона!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)


# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id

    # Если юзер отправил номер по кнопке
    if message.contact:
        print(message.contact)
        user_num = message.contact.phone_number
        # Регистрируем юзера
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        products = database.get_pr_buttons()
        bot.send_message(user_id, 'Выберите пункт меню:',
                        reply_markup=buttons.main_menu(products))
    # Если юзер отправил номер не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку!')
        # Возврат на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)


# Обработка выбора количества товара
@bot.callback_query_handler(lambda call: call.data in ['decrement', 'increment', 'to_cart', 'back'])
def choose_count(call):
    user_id = call.message.chat.id

    if call.data == 'increment':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_pr_count(
                                          database.get_exact_pr(
                                          users[user_id]['pr_name'])[3],
                                          'increment',
                                          users[user_id]['pr_count']))
        users[user_id]['pr_count'] += 1
    elif call.data == 'decrement':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_pr_count(
                                          database.get_exact_pr(
                                          users[user_id]['pr_name'])[3],
                                          'decrement',
                                          users[user_id]['pr_count']))
        users[user_id]['pr_count'] -= 1
    elif call.data == 'to_cart':
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        pr_name = database.get_exact_pr(users[user_id]['pr_name'])[1]
        database.add_to_cart(user_id, pr_name, users[user_id]['pr_count'])
        bot.send_message(user_id, 'Товар успешно помещен в корзину!')
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'back':
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))


# Обработка работы корзины
@bot.callback_query_handler(lambda call: call.data in ['cart', 'clear', 'order'])
def cart_handle(call):
    user_id = call.message.chat.id
    text = 'Ваша корзина:\n\n'

    if call.data == 'cart':
        user_cart = database.show_cart(user_id)
        total = 0.0

        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n'
                     f'------------------------\n')
            total += database.get_exact_price(i[1]) * i[2]
        text += f'Итого: {round(total, 2)}'
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, text, reply_markup=buttons.cart_buttons())
    elif call.data == 'clear':
        database.clear_cart(user_id)
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'order':
        text = text.replace('Ваша корзина:', f'Новый заказ!\nКлиент @{call.message.chat.username}\n')
        user_cart = database.show_cart(user_id)
        total = 0.0

        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n'
                     f'------------------------\n')
            total += database.get_exact_price(i[1]) * i[2]
        text += f'Итого: {round(total, 2)}'
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Отправьте локацию, куда доставить ваш заказ!',
                         reply_markup=buttons.loc_button())
        # Переход на этап получения локации
        bot.register_next_step_handler(call.message, get_loc, text)


# Этап получения локации
def get_loc(message, text):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {}
    if message.location:
        user_id = message.from_user.id
        users[user_id]['location'] = message.location
        users[user_id]['order_text'] = text

        # Считаем сумму заказа
        cart = database.show_cart(user_id)
        total = 0
        for item in cart:
            total += database.get_exact_price(item[1]) * item[2]

        bot.send_invoice(
            user_id,
            title='Оплата заказа',
            description='Ваш заказ: оплата доставки еды',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',  # замени на реальный токен
            currency='UZS',
            photo_url='https://play-lh.googleusercontent.com/vinYJkoh5f-UTTHgiV2DZ9YssEEfk69esYFrasVirZ5Wfp_-da5ahAel63pY-Q2IMnc=w240-h480-rw',
            photo_width=512,
            photo_height=512,
            photo_size=512,
            is_flexible=False,
            prices=[telebot.types.LabeledPrice(label='Общая сумма', amount=int(total * 100))],
            invoice_payload=json.dumps({'user_id': user_id})
        )
    else:
        bot.send_message(message.chat.id, 'Отправьте локацию по кнопке!')
        bot.register_next_step_handler(message, get_loc, text)


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.from_user.id
    order_text = users[user_id].get('order_text', '')
    loc = users[user_id].get('location')

    # Отправка админу
    bot.send_message('211029038', order_text)
    if loc:
        bot.send_location('211029038', latitude=loc.latitude, longitude=loc.longitude)

    database.make_order(user_id)
    database.clear_cart(user_id)

    bot.send_message(user_id, '✅ Оплата прошла успешно! Ваш заказ принят!',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(user_id, 'Выберите пункт меню:',
                     reply_markup=buttons.main_menu(database.get_pr_buttons()))


# Обработчик команды /admin
@bot.message_handler(commands=['admin'])
def admin(message):
   if message.from_user.id == 211029038:
       bot.send_message(admin_id, 'Добро пожаловать в админ панель!', reply_markup=buttons.admin_buttons())
       bot.register_next_step_handler(message, admin_choice)
   else:
       bot.send_message(user_id, 'У вас нету админ доступа!Введите команду /start')
def admin_choice(message):
    if message.text == 'Добавить товар':
        bot.send_message(admin_id, 'Чтобы добавить товар в базу, введите его в следующей последовательности:\n'
                                   'Название, описание, кол-во, цена, фото\n\n'
                                   'Пример:\n'
                                   'Картошка фри, вкусни, 500, 14000, https://kartoxa.jpg\n\n'
                                   '<a href="https://postimages.org/">Сайт</a> для загрузки фото.\n'
                                   'Пришлите мне прямую ссылку на фото товара!',
                         parse_mode='HTML')
        bot.register_next_step_handler(message, wait_for_product_input)

    elif message.text == 'Удалить товар':
        if database.check_pr():
            bot.send_message(admin_id, 'Выберите товар для удаления:', reply_markup=buttons.admin_pr_buttons(database.get_pr_buttons()))
            act = 'del'
            bot.register_next_step_handler(message, get_pr_name, act)
        else:
            bot.send_message(admin_id, 'Товаров в базе нет!')
            bot.register_next_step_handler(message, get_pr)
    elif message.text == 'Изменить товар':
        if database.check_pr():
            bot.send_message(admin_id, 'Выберите товар для изменения:',
                                 reply_markup=buttons.admin_pr_buttons(database.get_pr_buttons()))
            act = 'edit'
            bot.register_next_step_handler(message, get_pr_name, act)
        else:
            bot.send_message(admin_id, 'Товаров в базе нет!')
            bot.register_next_step_handler(message, get_pr)
    elif message.text == 'Назад в главное меню':
        start(message)

def wait_for_product_input(message):
     get_pr(message)


def get_pr_name(message, act):
    if message.text == 'Назад':
        bot.send_message(admin_id, 'Отмена операции', reply_markup=buttons.admin_buttons() )
        bot.register_next_step_handler(message, admin_choice)
    elif act == 'del':
        pr_name = message.text
        database.del_pr(pr_name)
        bot.send_message(admin_id, 'Удаление прошло успешно!', reply_markup=buttons.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)
    elif act == 'edit':
        pr_name = message.text
        admins[admin_id] = pr_name
        bot.send_message(admin_id, 'Какой атрибут вы хотите изменить?', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(admin_id, 'Выберите атрибут из списка:', reply_markup=buttons.attr_buttons())
@ bot.callback_query_handler(lambda call: call.data in ['name', 'des', 'count', 'price', 'photo'])

def get_attr(call):
    product = admins[admin_id]

    if call.data == 'name':
        attr = call.data
        bot.delete_message(chat_id=admin_id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новое название')
        # Переход на этап изменения
        bot.register_next_step_handler(call.message, pr_change, product, attr)
    elif call.data == 'des':
        attr = call.data
        bot.delete_message(chat_id=admin_id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новое описание')
        # Переход на этап изменения
        bot.register_next_step_handler(call.message, pr_change, product, attr)
    elif call.data == 'count':
        attr = call.data
        bot.delete_message(chat_id=admin_id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новое количество')
        # Переход на этап изменения
        bot.register_next_step_handler(call.message, pr_change, product, attr)
    elif call.data == 'price':
        attr = call.data
        bot.delete_message(chat_id=admin_id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новое описание')
        # Переход на этап изменения
        bot.register_next_step_handler(call.message, pr_change, product, attr)
    elif call.data == 'photo':
        attr = call.data
        bot.delete_message(chat_id=admin_id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Отправьте ссылку на новое фото')
        # Переход на этап изменения
        bot.register_next_step_handler(call.message, pr_change, product, attr)

def pr_change(message, product, attr):
    new_value = message.text

    if attr == 'price':
        database.change_pr(product, float(new_value), attr)
    else:
        database.change_pr(product, new_value, attr)
    bot.send_message(admin_id, 'Toвap ycпeшнo изменен!', reply_markup=buttons.admin_buttons())
        # Переход на этап выбора
    bot.register_next_step_handler(message, admin_choice)


def get_pr(message):
    admin_id = message.from_user.id
    parts = message.text.split(', ')

    if len(parts) != 5:
        bot.send_message(admin_id, 'Ошибка! Введите все 5 параметров через запятую:\n'
                                   'Название, описание, количество, цена, ссылка на фото')
        bot.register_next_step_handler(message, get_pr)
        return

    pr_name, pr_des, pr_count, pr_price, pr_photo = parts
    try:
        pr_count = int(pr_count)
        pr_price = float(pr_price)
        database.add_pr_to_db(pr_name, pr_des, pr_count, pr_price, pr_photo)
        bot.send_message(admin_id, 'Товар успешно добавлен!', reply_markup=buttons.admin_buttons())
    except ValueError:
        bot.send_message(admin_id, 'Ошибка! Количество и цена должны быть числами.')
        bot.register_next_step_handler(message, get_pr)


# Обработчик callback_data на товар
@bot.callback_query_handler(lambda call: int(call.data) in [i[0] for i in database.get_all_pr()])
def choose_product(call):
    user_id = call.message.chat.id
    pr_info = database.get_exact_pr(int(call.data))
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    bot.send_photo(user_id, photo=pr_info[-1], caption=f'<b>{pr_info[1]}</b>\n\n'
                                                       f'<b>Описание: </b>{pr_info[2]}\n'
                                                       f'<b>Количество: </b>{pr_info[3]}\n'
                                                       f'<b>Цена: </b>{pr_info[4]} сум\n',
                   parse_mode='HTML', reply_markup=buttons.choose_pr_count(pr_info[3]))
    users[user_id] = {'pr_name': pr_info[0], 'pr_count': 1}


# Запуск бота
bot.polling(non_stop=True)