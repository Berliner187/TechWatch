# -*- coding: UTF-8 -*-
import json
from datetime import datetime

import requests


def get_weather(city):
    if city is None:
        pass
    api_key_file = open('API_KEY.txt')
    api_key = api_key_file.readline()

    filename = "weather_data.json"

    # Функция для чтения данных из файла
    def load_data():
        try:
            with open(filename, "r") as file:
                data_response = json.load(file)
        except FileNotFoundError:
            data_response = {}
        return data_response

    # Функция для записи данных в файл
    def save_data(data_response):
        with open(filename, "w") as file:
            json.dump(data_response, file)

    # Функция для получения данных о погоде
    def get_weather_data():
        def get_sunrise_and_sunset_times(response_data):
            sunrise_unix = response_data['sys']['sunrise']
            sunset_unix = response_data['sys']['sunset']
            _sunrise = datetime.fromtimestamp(sunrise_unix)
            _sunset = datetime.fromtimestamp(sunset_unix)
            time_sunrise = _sunrise.strftime("%H:%M")
            time_sunset = _sunset.strftime("%H:%M")
            return time_sunrise, time_sunset

        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
        data_from_openweather = json.loads(response.text)
        temperature = str(round(data_from_openweather['main']['temp'] - 273.15, 1)).replace('.', ',')
        cloudiness = [data_from_openweather['weather'][0]['main'], data_from_openweather['weather'][0]['description']]
        humidity = data_from_openweather['main']['humidity']
        sunrise, sunset = get_sunrise_and_sunset_times(data_from_openweather)

        # Данные о погоде в виде списка
        return {
            "city": city,
            "temperature": f'{temperature} °C',
            "sky": cloudiness,
            "humidity": f'{humidity}%',
            "sunrise": sunrise,
            "sunset": sunset
        }

    # Получаем текущее время
    now = datetime.now()

    # Загружаем данные из файла
    data = load_data()

    # Если данные уже есть и последний запрос был менее 20 минут назад
    if "last_request" in data and "weather_data" in data and (
            now - datetime.strptime(data["last_request"], "%Y-%m-%d %H:%M:%S.%f")).seconds < 1200:
        # Используем уже имеющиеся данные
        weather_data = data["weather_data"]
    else:
        # Получаем новые данные о погоде
        weather_data = get_weather_data()
        # Сохраняем данные и время запроса в файл
        data["last_request"] = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        data["weather_data"] = weather_data
        save_data(data)

    weather_data["time_last_request"] = data["last_request"]

    return weather_data
