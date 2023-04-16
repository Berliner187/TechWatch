const quoteBlock = document.querySelector('.quote-block');
const quoteText = document.querySelector('.quote-text');
const quoteAuthor = document.querySelector('.quote-author');

// Функция для получения случайной цитаты
function getQuote() {
// Отправляем GET-запрос на API Flask
fetch('/quote')
    .then(response => response.json())
    .then(data => {
        quoteText.textContent = data.text;
        quoteAuthor.textContent = '— ' + data.author;
    })
    .catch(error => {
    console.error(error);
    });
}

const getQuoteBtn = document.querySelector('#get-quote-btn');

getQuoteBtn.addEventListener('click', () => {
fetch('/quote') // обращаемся к Flask-маршруту, который возвращает случайную цитату
    .then(response => response.json())
    .then(data => {
        quoteText.textContent = data.text;
        quoteAuthor.textContent = '— ' + data.author;
        quoteText.classList.add('animate'); // добавляем класс animate для анимации
        setTimeout(() => {
            quoteText.classList.remove('animate'); // убираем класс animate через 1 секунду
        }, 1000);
        })
        .catch(error => {
        console.error(error);
        });
});

getQuote();