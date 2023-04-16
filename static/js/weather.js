const city = document.getElementById('city');
const temperature = document.getElementById('temperature');
const sky = document.getElementById('sky');
const sky_sub = document.getElementById('sky_sub');
const humidity = document.getElementById('humidity_sub');
const sunrise = document.getElementById('sunrise_sub');
const sunset = document.getElementById('sunset_sub');
const lastUpdate = document.getElementById('last_update');

$(document).ready(function(){
    const savedCity = "{{ weather_info[0] }}"; // сохраненный город на бэке

    if (savedCity) { // Проверяем, есть ли сохраненный город на бэке
    const cityDiv = $('#city');
    cityDiv.html(savedCity); // Выводим сохраненный город
    } else {
    const cityInput = $('<input type="text" id="city-input">'); // Cоздаем поле ввода
    const cityDiv = $('#city');
    cityDiv.append(cityInput); // Добавляем поле ввода в div

    cityInput.on('change', function(){ // Обработка события на изменение поля ввода
        const inputCity = cityInput.val().trim();

        if(inputCity){ // Проверяем, что значение поля ввода не пустое
        cityDiv.html(inputCity); // Заменяем div на введенный город
        }
    });
    }
});

function formatDateString(dateStr) {
    console.log(dateStr);
    const date = new Date(dateStr);
    const now = new Date();

    // Разница между датами в миллисекундах
    const diffMs = now.getTime() - date.getTime();
    const diffMin = Math.round(diffMs / (1000 * 60));
    const diffHours = Math.round(diffMin / 60);
    const diffDays = Math.round(diffHours / 24);
    
    // Строка с результатом формата типа: "минуту назад", "15 минут назад", "вчера"
    if (diffMin <= 1) {
        return 'только что';
    } else if (diffMin === 1) {
        return 'минуту назад';
    } else if (diffMin < 60) {
        return `${diffMin} минут назад`;
    } else if (diffHours < 24) {
        return `${diffHours} ${declOfNum(diffHours, ['час', 'часа', 'часов'])} назад`;
    } else if (diffDays === 1) {
        return 'вчера';
    } else {
        const options = {
        day: 'numeric',
        month: 'long'
        };
        return date.toLocaleDateString('ru', options);
    }
}

function declOfNum(n, text_forms) {
    n = Math.abs(n) % 100;
    const n1 = n % 10;
    if (n > 10 && n < 20) return text_forms[2];
    if (n1 > 1 && n1 < 5) return text_forms[1];
    if (n1 === 1) return text_forms[0];
    return text_forms[2];
}

function getWeather() {
    fetch('/weather')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        city.textContent = data['city'];
        temperature.textContent = data['temperature'];
        sky.textContent = data['sky'][0];
        sky_sub.textContent = data['sky'][1];
        humidity.textContent = data['humidity'];
        sunrise.textContent = data['sunrise'];
        sunset.textContent = data['sunset'];

        const dateStr = data['time_last_request'];
        const prettyDate = formatDateString(dateStr);

        lastUpdate.textContent = prettyDate;
        console.log(data['time_last_request']);
    })
}

getWeather();
setInterval(getWeather, 1000);
