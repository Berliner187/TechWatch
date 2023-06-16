// Функция для установки значения cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Функция для чтения значения cookie
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Функция для удаления значения cookie
function eraseCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
}

// При загрузке страницы восстанавливаем выбранный цвет из cookie
window.addEventListener('load', function() {
    var selectedColor = getCookie('selectedColor');
    if (selectedColor) {
        document.body.style.backgroundColor = selectedColor;
        $('.note-button').css('background-color', selectedColor);
        $('.quote-button').css('background-color', selectedColor);
        $('.footer-developer').css('background-color', selectedColor);
        $('#notesList').css('color', selectedColor);
    }
});

// Функция для изменения фона страницы
const changeBackgroundColor = (color) => {
    document.body.style.backgroundColor = color;
    $('.note-button').css('background-color', color);
    $('.quote-button').css('background-color', color);
    $('.footer-developer').css('background-color', color);
    $('#notesList').css('color', color);
};

const colorButtons = document.querySelectorAll('.color-buttons button'); // Получаем все кнопки цветов

// Функция для сохранения выбранного цвета в cookie
const saveColorToCookie = (color) => {
    document.cookie = `selectedColor=${color}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;
};

// Обработчик клика на кнопках цветов
colorButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const color = e.target.dataset.color; // Получаем выбранный цвет из атрибута data-color
        changeBackgroundColor(color); // Изменяем фон страницы
        saveColorToCookie(color); // Сохраняем выбранный цвет в cookie
    });
});

$(document).ready(function() {
    // Получение текущего выбранного цвета из cookie
    var currentColor = getCookie('background_color');
    if (currentColor) {
        $('body').css('background-color', currentColor);
    }

    // Обработка клика на кнопках цветов
    $(".color-button").click(function() {
        var color = $(this).data("color");
        $('body').css('background-color', color);
        setCookie('background_color', color, 7); // Сохранение цвета в cookie на 7 дней
    });
});

// Функция для получения значения cookie по имени
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

// Функция для установки значения cookie
function setCookie(name, value, days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    var expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + "; " + expires + "; path=/";
}

document.addEventListener('DOMContentLoaded', function() {
    // Костыль
    var style = document.createElement('style');
    style.innerHTML = '.color-buttons { display: none; }';
    document.head.appendChild(style);

    var icon = document.querySelector('.icon');
    var colorButtons = document.querySelector('.color-buttons');

    // Обработчик клика на иконку параметров
    icon.addEventListener('click', function() {
    if (colorButtons.style.display === 'block') {
        colorButtons.style.display = 'none';
    } else {
        colorButtons.style.display = 'block';
    }
    });

    // Обработчик клика на кнопки
    var colorButtonsArray = Array.from(document.querySelectorAll('.color-button'));
    colorButtonsArray.forEach(function(button) {
    button.addEventListener('click', function() {
        var color = this.dataset.color;
        document.body.style.backgroundColor = color;
        document.cookie = 'background_color=' + color;
    });
    });
});
