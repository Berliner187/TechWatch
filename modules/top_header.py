from datetime import datetime
import socket
import psutil


def hostname():
    return socket.gethostname()


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


def battery():
    def get_battery_time_left():
        _battery = psutil.sensors_battery()
        if battery.secsleft > 0:
            time_left_sec = _battery.secsleft
            hours = time_left_sec // 3600
            minutes = (time_left_sec % 3600) // 60
            time_left_str = f'{hours} ч {minutes} мин.'
            if _battery.secsleft >= 4294967295:
                return ''
            else:
                return time_left_str
        else:
            return ''
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


def header_controller():
    return {
        "hostname": hostname(),
        "greeting": greeting(),
        "battery": battery()
    }
