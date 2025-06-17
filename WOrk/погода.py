import requests

URL = "https://cbu.uz/ru/arkhiv-kursov-valyut/json/"

def get_rates():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка при получении данных с ЦБ")
        return []

def find_rate(currency_code, rates):
    for rate in rates:
        if rate['Ccy'] == currency_code:
            return float(rate['Rate'])
    return None

def convert_currency(amount, from_code, to_code, rates):
    if from_code == to_code:
        return amount

    # Курс для изначальной валюты
    from_rate = find_rate(from_code, rates) if from_code != "UZS" else 1.0
    # Курс для валюты, в которую конвертируем
    to_rate = find_rate(to_code, rates) if to_code != "UZS" else 1.0

    if from_rate is None or to_rate is None:
        return None

    # Переводим сначала сумму в UZS, затем в нужную валюту
    amount_in_uzs = amount * from_rate
    converted_amount = amount_in_uzs / to_rate
    return converted_amount

if __name__ == "__main__":
    rates = get_rates()
    if not rates:
        exit()

    amount = float(input("Введите сумму: "))
    from_code = input("Из валюты (например, USD): ").upper()
    to_code = input("В валюту (например, EUR): ").upper()

    result = convert_currency(amount, from_code, to_code, rates)
    if result is not None:
        print(f"{amount} {from_code} = {round(result, 2)} {to_code}")
    else:
        print("Не удалось выполнить конвертацию. Проверьте коды валют.")
