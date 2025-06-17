import sql3
def register_client():
    id = int(input("Введите ваш ID: "))
    if sql3.check_user(id):
        print('Добро пожаловать!')
    else:
        print('Привет! Давай начнем регистрацию!')
        full_name = input('Введи полное имя:  ')
        print('Отлично теперь буду звать тебя:', full_name)


        phone = input('Введите номер телефона: ')
        sql3.add_client(id, full_name, phone)
        print('✅ Регистрация завершена!')
    return id
def account(id):
    client = sql3.get_client(id)
    if client:
        print("\n--- Личный кабинет ---")
        print(f"ID: {client[0]}")
        print(f"ФИО: {client[1]}")
        print(f"Телефон: {client[2]}")
        print(f"Баланс: {client[3]:.2f} UZS")
        print("----------------------\n")
    else:
        print("Ошибка: клиент не найден.")
def deposit(id):
    amount = float(input("Введите сумму для пополнения: "))
    if amount <= 0:
        print("Сумма должна быть положительной!")
        return
    sql3.update_balance(id, amount)
    print('Баланс успешно пополнен на:', amount, 'UZS')

def withdraw(id):
        amount = float(input("Введите сумму для снятия: "))
        if amount <= 0:
            print("Сумма должна быть положительной!")
            return
        current_balance = sql3.get_balance(id)
        if current_balance is None:
            print("Ошибка: клиент не найден.")
            return
        if amount > current_balance:
            print("Недостаточно средств на балансе!")
            return
        sql3.update_balance(id, -amount)
        print(f"Снято {amount:.2f} UZS с баланса")


def start():
    current_id = None
    while True:
        print("\n🔸 Главное меню:")
        print("1. Войти или зарегистрироваться")
        print("2. Мой аккаунт")
        print("3. Пополнить баланс")
        print("4. Снять деньги")
        print("0. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":

            current_id = register_client()
        elif choice == '2':
            if current_id is not None:
                account(current_id)
            else:
                print("❗ Сначала войдите или зарегистрируйтесь!")
        elif choice == "3":
            if current_id is not None:
                deposit(current_id)
            else:
                print("Сначала войдите или зарегистрируйтесь!")

        elif choice == "4":
            if current_id is not None:
                withdraw(current_id)
            else:
                print("Сначала войдите или зарегистрируйтесь!")


        elif choice == "0":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор!")

    # Запуск
start()






