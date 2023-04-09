from flask import Flask, render_template, jsonify
import time
from datetime import datetime
import platform
import os
import sys
import socket
import random

import psutil
import requests
import json

import quotes_obs
import weather_forecast


app = Flask(__name__)


def greeting():
    hms = datetime.today()
    time_now = hms.hour * 3600 + hms.minute * 60 + hms.second  # Время в секундах
    if 14400 <= time_now < 43200:
        return 'Good Morning'
    elif 43200 <= time_now < 61200:
        return 'Good Afternoon'
    elif 61200 <= time_now <= 86399:
        return 'Good Evening'
    elif 0 <= time_now < 14400:
        return 'Good Night'


@app.route('/')
def index():
    global size_gb, free_gb, used_percent, occupied

    city = 'Tver'

    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    day_week = now.strftime("%A")

    # Системная информация
    os_info = f"{platform.system()} {platform.release()}"
    cpu_percent = psutil.cpu_percent(percpu=True)

    mem = psutil.virtual_memory()
    mem_usage = mem.used / 1024 / 1024 / 1024
    total_memory = mem.total / (1024 ** 3)
    memory_percent = mem.percent

    memory_indicators = {
        "total_memory": total_memory,
        "memory_usage": mem_usage,
        "memory_percent": memory_percent
    }

    disk = psutil.disk_usage('/')
    os_name = f"{psutil.Process().name()} ({psutil.Process().pid})"

    # Аккумулятор
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    # Hostname
    hostname = socket.gethostname()

    if plugged:
        battery_level = 'charge'
    else:
        if 5 < percent <= 20:
            battery_level = 1
        elif 20 < percent <= 40:
            battery_level = 2
        elif 40 < percent <= 70:
            battery_level = 3
        elif 70 < percent <= 100:
            battery_level = 4
        else:
            battery_level = 0

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
        "used_percent": used_percent, "occupied": occupied}

    return render_template(
        'index.html',
        greeting=greeting(),
        time=now.strftime("%H:%M"),
        date={"date": date, "day_week": day_week},
        os_info=os_info,
        processor_info=platform.processor(),
        cpu_percent=cpu_percent, disk=disk, os_name=os_name,
        weather_info=weather_forecast.get_weather(city),
        battery={"battery_level": battery_level, "percent": percent},
        disk_info=disk_info,
        hostname=hostname,
        memory=memory_indicators,
        disks_indicators=disks_indicators
    )


def disk_space():
    # Disks
    disk_partitions = psutil.disk_partitions()
    disks = []
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        size_gb = usage.total
        free_gb = usage.free
        occupied = size_gb - free_gb
        used_percent = usage.percent
        disks.append([size_gb, free_gb, occupied, used_percent])

    # Данные внутри контейнера с облигацией (при раскрытии)
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


@app.route('/disk-c')
def get_c_disk():
    return jsonify(disk_space()[0])


@app.route('/disk-d')
def get_d_disk():
    return jsonify(disk_space()[1])


@app.route('/cpu')
def cpu():
    cpu_percent = psutil.cpu_percent()
    return jsonify(cpu_percent=cpu_percent)


@app.route('/battery')
def get_battery():
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
        elif 70 < percent <= 100:
            battery_level = 4
        else:
            battery_level = 0
    battery_info = {
        "battery_level": battery_level,
        "percent": percent
    }
    return jsonify(battery_info)


@app.route('/memory-usage')
def memory_usage():
    memory = psutil.virtual_memory()
    memory_use = round(memory.used / 1024 / 1024 / 1024, 2)
    memory_total = round(memory.total / (1024 ** 3), 2)
    memory_percent = memory.percent

    memory_indicators_dict = {
        "total_memory": memory_total,
        "memory_usage": memory_use,
        "memory_percent": memory_percent
    }
    return jsonify(memory_indicators_dict)


@app.route('/quote')
def quote():
    quotes = quotes_obs.quotes

    random_quote = random.choice(quotes)
    return jsonify(random_quote)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
