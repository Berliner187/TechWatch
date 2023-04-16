from flask import Flask, render_template, jsonify, request, make_response
import time
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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'random_secret_key'


notes = []
s = 0


class SystemIndicators:
    def cpu_info(self):
        return

    def discs_info(self):
        return

    def battery_info(self):
        return

    def memory_info(self):
        return


def greeting():
    hms = datetime.today()
    time_now = hms.hour * 3600 + hms.minute * 60 + hms.second
    if 14400 <= time_now < 43200:
        return 'Good Morning'
    elif 43200 <= time_now < 61200:
        return 'Good Afternoon'
    elif 61200 <= time_now <= 86399:
        return 'Good Evening'
    elif 0 <= time_now < 14400:
        return 'Good Night'


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


def get_disks_info():
    size_gb, free_gb, used_percent, occupied = 0, 0, 0, 0
    disk_partitions = psutil.disk_partitions()

    disk_info = []
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        size_gb = usage.total / (1024 ** 3)
        free_gb = usage.free / (1024 ** 3)
        occupied = size_gb - free_gb
        used_percent = usage.percent
        disk_info.append(f"{partition.device} {size_gb - free_gb:.2f} GB/{size_gb:.2f} GB ({used_percent}%)")

    disks_indicators = {
        "total_size": size_gb, "free_size": free_gb,
        "used_percent": used_percent, "occupied": occupied,
        "disk_info": disk_info
    }

    return disks_indicators


def get_battery_indicators():
    # Аккумулятор
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    if plugged:
        battery_level = 'charge'
    else:
        if 5 < percent <= 20:
            battery_level = 1
        elif 20 < percent <= 40:
            battery_level = 2
        elif 40 < percent <= 70:
            battery_level = 3
        elif 70 < percent <= 90:
            battery_level = 4
        elif 90 < percent <= 100:
            battery_level = 5
        else:
            battery_level = 0

    battery_indicators = {
        "battery_level": battery_level, "percent": percent,
        "time_left": get_battery_time_left()
    }
    return battery_indicators


@app.route('/')
@app.route('/dashboard')
def index():
    city = 'Moscow'

    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    day_week = now.strftime("%A")

    # Системная информация
    os_info = f"{platform.system()} {platform.release()}"
    os_name = f"{psutil.Process().name()} ({psutil.Process().pid})"

    cpu_percent = psutil.cpu_percent(percpu=True)

    # Hostname
    hostname = socket.gethostname()

    current_color = request.cookies.get('color')

    # Дата и день недели
    date_indicators = {
        "date": date, "day_week": day_week
    }

    return render_template(
        'index.html',
        greeting=greeting(),
        time=now.strftime("%H:%M"),
        date=date_indicators,
        os_info=os_info,
        processor_info=platform.processor(),
        cpu_percent=cpu_percent,
        os_name=os_name,
        weather_info=weather_forecast.get_weather(city),
        battery=get_battery_indicators(),
        disk_info=get_disks_info()["disk_info"],
        hostname=hostname,
        memory=get_memory_info()
    )


def disk_space():
    # Диски
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
    hidden_data_dict = {}
    for i, disk_data in enumerate(disks):
        hidden_data_dict['total_size'] = disk_data[0]
        hidden_data_dict['free_size'] = disk_data[1]
        hidden_data_dict['occupied'] = disk_data[2]
        hidden_data_dict['used_percent'] = disk_data[3]

        disks_array.append(hidden_data_dict)
        hidden_data_dict = {}
    return disks_array


@app.route('/weather')
def weather():
    weather_file = open('weather_data.json')
    response_data = json.load(weather_file)
    data = weather_forecast.get_weather(response_data["weather_data"]["city"])
    return jsonify(data)


@app.route('/disk-c')
def get_c_disk():
    return jsonify(disk_space()[0])


@app.route('/disk-d')
def get_d_disk():
    return jsonify(disk_space()[1])


@app.route('/cpu_percent')
def get_cpu_percent():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return jsonify(cpu_percent=cpu_percent)


@app.route('/battery')
def get_battery():
    return jsonify(get_battery_indicators())


@app.route('/memory-usage')
def memory_usage():
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


@app.route('/quote')
def quote():
    quotes = quotes_obs.quotes
    random_quote = random.choice(quotes)
    return jsonify(random_quote)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
