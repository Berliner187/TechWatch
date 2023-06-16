from flask import Flask, render_template, jsonify, request, make_response, session, redirect
from datetime import datetime
import platform
import os
import sys
import socket
import random

import psutil
import json

import quotes_obs
import weather_forecast
import modules.currency as currency_obs

import modules.customization as customization
import modules.top_header as top_header
import modules.system_indicators as system_indicators


from version import __version__


def generate_secret_key():
    _secret_key = ''
    symbols = '1234567890qwertyuiopasdfghjklzxcvbnm'
    for i in range(16):
        _secret_key += random.choice(symbols)
    return _secret_key


app = Flask(__name__)
app.config['SECRET_KEY'] = generate_secret_key()


notes = []


def read_city():
    file_with_city = 'city.txt'

    if os.path.exists(file_with_city):
        with open(file_with_city) as file:
            return file.readline()
    else:
        print(f'Make file {file_with_city}.')
        with open(file_with_city, 'w') as file:
            file.write('Moscow')
        return


def get_battery_time_left():
    battery = psutil.sensors_battery()
    if battery.secsleft > 0:
        time_left_sec = battery.secsleft
        hours = time_left_sec // 3600
        minutes = (time_left_sec % 3600) // 60
        time_left_str = f'{hours} ч {minutes} мин.'
        if battery.secsleft >= 4294967295:
            return ''
        else:
            return time_left_str
    else:
        return ''


def get_memory_info():
    memory = psutil.virtual_memory()
    memory_use = round(memory.used / 1024 / 1024 / 1024, 2)
    memory_total = round(memory.total / (1024 ** 3), 2)
    memory_percent = memory.percent

    memory_indicators_dict = {
        "total_memory": memory_total,
        "memory_usage": memory_use,
        "memory_percent": memory_percent
    }

    return memory_indicators_dict


def disk_space():
    """
    Информация о дисках
    :return: {total_size, free_size, occupied, used_percent}
    """
    disk_partitions = psutil.disk_partitions()
    disks = []
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        size_gb = usage.total
        free_gb = usage.free
        occupied = size_gb - free_gb
        used_percent = usage.percent
        disks.append([size_gb, free_gb, occupied, used_percent])

    disks_array = []
    disks_indicators_dict = {}

    for i, disk_data in enumerate(disks):
        disks_indicators_dict['total_size'] = disk_data[0]
        disks_indicators_dict['free_size'] = disk_data[1]
        disks_indicators_dict['occupied'] = disk_data[2]
        disks_indicators_dict['used_percent'] = disk_data[3]
        disks_array.append(disks_indicators_dict)
        disks_indicators_dict = {}

    return disks_array


def get_datetime():
    now = datetime.now()
    _date = now.strftime("%d/%m/%Y")
    _day_week = now.strftime("%A")
    return {
        "date": _date,
        "day_week": _day_week
    }


@app.route('/')
@app.route('/dashboard')
def index():
    city = read_city()

    # Системная информация
    system_information = system_indicators.SystemIndicators().get_system_indicators()

    return render_template(
        'index.html',
        top_header=top_header.header_controller(),
        date_time=get_datetime(),
        system_information=system_information,
        weather_info=weather_forecast.get_weather(city),
        currency_info=currency_obs.load_currency_info_from_json(),
        currency_last_update=currency_obs.get_last_parsing_time(),
        colors=customization.themes(),
        current_version=__version__
    )


@app.route
def date():
    return jsonify()


@app.route('/currency')
def currency_response():
    return jsonify(currency_obs.get_last_parsing_time())


@app.route('/weather')
def weather_response():
    weather_file = open('weather_data.json')
    response_data = json.load(weather_file)
    data = weather_forecast.get_weather(response_data["weather_data"]["city"])
    return jsonify(data)


@app.route('/disks-info')
def disks_info_response():
    return jsonify(disk_space())


@app.route('/cpu_percent')
def get_cpu_percent_response():
    cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
    return jsonify(cpu_percent=cpu_percent)


@app.route('/battery')
def get_battery_response():
    return jsonify(top_header.battery())


@app.route('/memory-usage')
def memory_usage_response():
    return jsonify(get_memory_info())


@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form['note']
    notes.append(note)
    return jsonify({'result': 'success'})


@app.route('/get_notes', methods=['GET'])
def get_notes():
    return jsonify({'notes': notes})


@app.route('/delete_note', methods=['POST'])
def delete_note():
    note = request.form['note']
    notes.remove(note)
    return jsonify({'result': 'success'})


@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
    if request.method == 'POST':
        request_data = request.get_json()
        quote = {'text': request_data['text'], 'author': request_data['author']}
        quotes_obs.quotes.append(quote)
        return jsonify(quotes_obs.quotes)
    else:
        return jsonify(quotes_obs.quotes)


# Удалить цитату
@app.route('/quotes/<int:index_q>', methods=['DELETE'])
def delete_quote(index_q):
    try:
        del quotes_obs.quotes[index_q]
    except IndexError:
        return jsonify({'error': 'Цитата не найдена'}), 404
    return jsonify({'message': 'Цитата удалена'}), 200


@app.route('/quote')
def quote_resp():
    # Костыль, который убирает ошибку в JS
    session.permanent = True
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='None',
    )

    selected_quotes = session.get('selected_quotes', [])
    _quotes = quotes_obs.quotes.copy()
    if not selected_quotes:
        selected_quotes = _quotes
    random_quote = random.choice(selected_quotes)
    selected_quotes.remove(random_quote)
    if not selected_quotes:
        selected_quotes = _quotes
    session['selected_quotes'] = selected_quotes
    return jsonify(random_quote)


@app.route('/manage-quotes')
def manage_quotes():
    return render_template(
        'quotes.html',
        top_header=top_header.header_controller(),
        quotes=quotes_obs.quotes,
        colors=customization.themes(),
        current_version=__version__
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
