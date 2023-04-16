function updateBatteryLevel() {
    fetch('/battery')
    .then(response => response.json())
    .then(data => {
        document.getElementById('battery-percent').textContent = `${data.percent}%`;
        // Смена иконки батареи
        let imgElem = document.getElementById('battery-level-img');
        imgElem.src = 'static/img/battery-' + data.battery_level + '.png';

        document.getElementById('battery_time_left').textContent = data.time_left;
    });
}

setInterval(updateBatteryLevel, 3000);