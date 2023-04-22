from flask import Flask, render_template, jsonify, request, make_response, session
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
app.config['SECRET_KEY'] = 'Dn8dbs8182DSBH8s'


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


def get_battery_indicators():
    # Аккумулятор
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    if plugged:
        battery_status = 'charge'
    else:
        battery_status = 'pass'

    if 5 < percent <= 20:
        battery_level = 1
    elif 20 < percent <= 50:
        battery_level = 2
    elif 50 < percent <= 70:
        battery_level = 3
    elif 70 < percent <= 90:
        battery_level = 4
    elif 90 < percent <= 100:
        battery_level = 5
    else:
        battery_level = 0

    battery_indicators = {
        "battery_icon": f'{battery_status}-{battery_level}',
        "percent": percent,
        "time_left": get_battery_time_left()
    }

    return battery_indicators


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
        colors=customization.themes(),
        current_version=__version__
    )


@app.route
def date():
    return jsonify()


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
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return jsonify(cpu_percent=cpu_percent)


@app.route('/battery')
def get_battery_response():
    return jsonify(get_battery_indicators())


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


# Получить список цитат
@app.route('/quotes', methods=['GET'])
def get_quotes():
    return jsonify(quotes_obs.quotes)


@app.route('/quotes', methods=['POST'])
def add_quote():
    data = request.get_json()
    quote = data.get('quote')
    if not quote:
        return jsonify({'error': 'Цитата не может быть пустой'}), 400
    quotes_obs.quotes.append(quote)
    return jsonify({'message': 'Цитата добавлена'}), 201


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
    selected_quotes = session.get('selected_quotes', [])
    _quotes = [quote for quote in quotes_obs.quotes if quote not in selected_quotes]
    if not _quotes:
        selected_quotes.clear()
        _quotes = quotes_obs.quotes
    random_quote = random.choice(_quotes)
    selected_quotes.append(random_quote)
    session['selected_quotes'] = selected_quotes
    return jsonify(random_quote)


@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
    if request.method == 'POST':
        quote = request.json['quote']
        quotes_obs.quotes.append(quote)
        return jsonify({'message': 'Цитата успешно добавлена!'})
    else:
        return jsonify(quotes_obs.quotes)


@app.route('/manage-quotes')
def manage_quotes():
    return render_template('quotes.html', quotes=quotes_obs.quotes)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
