import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# URL страницы для парсинга
url = 'https://www.banki.ru/products/currency/cb/'

# Отправляем GET-запрос и получаем содержимое страницы
response = requests.get(url)
content = response.content

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(content, 'html.parser')

# Путь к файлу JSON
json_file_path = 'currency_info.json'


def get_currency_info():
    # Находим все элементы <tr> с атрибутом data-test="currency-table-row"
    currency_rows = soup.find_all('tr', attrs={'data-test': 'currency-table-row'})

    # Массив для хранения информации о валютах
    currency_info_array = []

    # Итерируемся по каждому элементу и получаем значения нужных <td>
    for currency_row in currency_rows:
        currency_name = currency_row.get('data-currency-name')
        td_elements = currency_row.find_all('td')
        if len(td_elements) >= 5:
            first_td = td_elements[0].text.strip()
            third_td = td_elements[2].text.strip()
            course = td_elements[3].text.strip()
            delta = td_elements[4].text.strip()

            # Создаем словарь с информацией о валюте
            currency_info = {
                'Currency Name': currency_name,
                'Country code': first_td,
                'Course': str(round(float(course), 2)).replace('.', ',') + ' ₽',
                'Delta': delta
            }

            # Добавляем словарь в массив
            currency_info_array.append(currency_info)
        else:
            print("Не удалось найти достаточно <td> элементов")

    # Обновляем время последнего парсинга
    last_parsing_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Создаем словарь с данными для JSON
    data = {
        'last_parsing_time': last_parsing_time,
        'currency_info_array': currency_info_array
    }

    # Сохраняем данные в JSON файл
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file)

    return currency_info_array


def get_last_parsing_time():
    def read_last_parsing_time_from_json():
        json_file_path = 'currency_info.json'

        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                last_parsing_time = data.get('last_parsing_time')
                if last_parsing_time:
                    last_parsing_time = datetime.fromisoformat(last_parsing_time)
                    current_time = datetime.now()
                    time_difference = current_time - last_parsing_time
                    minutes = int(time_difference.total_seconds() / 60)
                    if minutes == 0:
                        return "Только что"
                    else:
                        return f"{minutes} мин назад"

        except FileNotFoundError:
            return None

    last_parsing_time = read_last_parsing_time_from_json()
    if last_parsing_time:
        return last_parsing_time
    else:
        return "Last parsing time not found or JSON file does not exist"


def load_currency_info_from_json():
    last_parsing_time = None

    # Читаем данные из JSON файла, если он существует
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            last_parsing_time = data.get('last_parsing_time')
            currency_info_array = data.get('currency_info_array', [])
    except FileNotFoundError:
        currency_info_array = []

    if last_parsing_time is not None:
        current_time = datetime.now()
        time_diff = current_time - datetime.strptime(last_parsing_time, '%Y-%m-%d %H:%M:%S')

        if time_diff.total_seconds() / 60 >= 20:
            currency_info_array = get_currency_info()

    else:
        currency_info_array = get_currency_info()

    return currency_info_array


currency_info_array = load_currency_info_from_json()
