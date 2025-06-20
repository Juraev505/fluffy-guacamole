from telebot import types


# Кнопка отправки номера
def num_button():
    # Создание пространства
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создание самих кнопок
    but1 = types.KeyboardButton('Отправить номер телефона📞', request_contact=True)
    # Добавление кнопок в пространство
    kb.add(but1)

    return kb


# Кнопка отправки локации
def loc_button():
    # Создание пространства
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создание самих кнопок
    but1 = types.KeyboardButton('Отправить геопозицию📍', request_location=True)
    # Добавление кнопок в пространство
    kb.add(but1)

    return kb


# Кнопки главного меню
def main_menu(products):
    # Создание пространства
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создание самих кнопок
    cart = types.InlineKeyboardButton(text='Корзина🛒',
                                      callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=i[1],
                                               callback_data=i[0])
                    for i in products]
    # Добавление кнопок в пространство
    kb.add(*all_products)
    kb.row(cart)

    return kb


# Кнопки выбора количества
def choose_pr_count(pr_amount, plus_or_minus='', amount=1):
    # Создание пространства
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создание сами кнопок
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    to_cart = types.InlineKeyboardButton(text='Добавить в корзину',
                                         callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')

    # Алгоритм изменения кол-ва
    if plus_or_minus == 'increment':
        if amount <= pr_amount:
            count = types.InlineKeyboardButton(text=str(amount+1),
                                               callback_data=str(amount+1))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            count = types.InlineKeyboardButton(text=str(amount-1),
                                               callback_data=str(amount-1))

    # Добавление кнопок в пространство
    kb.add(minus, count, plus)
    kb.row(back, to_cart)

    return kb


# Кнопки корзины
def cart_buttons():
    # Создание пространства
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создание самих кнопок
    order = types.InlineKeyboardButton(text='Оформить заказ🧾', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину🗑️',
                                       callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    # Добавление кнопок в пространство
    kb.add(order, clear)
    kb.row(back)

    return kb
def admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Добавить товар')
    but2 = types.KeyboardButton('Удалить товар')
    but3 = types.KeyboardButton('Изменить товар')
    but4 = types.KeyboardButton('Назад в главное меню')
    kb.add(but1, but2, but3)
    kb.row(but4)
    return kb


from telebot import types


def admin_pr_buttons(products):  # products — список товаров
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    all_products = []

    for pr in products:
        all_products.append(types.KeyboardButton(pr[1]))  # pr[1] — название товара

    kb.add(*all_products)  # распаковка списка кнопок
    kb.add(types.KeyboardButton('Назад'))

    return kb


def attr_buttons():
    kb = types.InlineKeyboardMarkup(row_width=2)
    name = types.InlineKeyboardButton(text='Название', callback_data='name')
    des = types.InlineKeyboardButton(text='Описание', callback_data='des')
    count = types.InlineKeyboardButton(text='Количевство', callback_data='count')
    price = types.InlineKeyboardButton(text='Цена', callback_data='price')
    photo = types.InlineKeyboardButton(text='Фото', callback_data='photo')
    kb.add(name, des, count, price)
    kb.row(photo)
    return kb