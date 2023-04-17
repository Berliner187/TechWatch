// Функция для обновления списка заметок на фронте
function updateNotesList() {
    $.get('/get_notes', function(data) {
        var notes = data.notes;
        var notesList = $('#notesList');
        notesList.empty();  // Очистка списка заметок
        for (var i = 0; i < notes.length; i++) {
            var noteItem = '<li class="noteItem">' + notes[i] + '</li>';  // Создание элемента заметки
            var deleteNoteButton = '<button class="deleteNoteButton" data-note="' + notes[i] + '"></button>';  // Создание кнопки удаления заметки
            notesList.append(noteItem + deleteNoteButton);  // Добавление заметки и кнопки в список
        }
    });
}
// Обработка события отправки формы
$('#addNoteForm').on('submit', function(event) {
    event.preventDefault();  // Отмена стандартного поведения формы
    var note = $('#noteInput').val();  // Получение значения заметки из поля ввода
    $.post('/add_note', {note: note}, function(data) {
        updateNotesList();  // Вызов функции обновления списка заметок на фронтенде
        $('#noteInput').val('');  // Очистка поля ввода
    });
});
// Обработка события клика на кнопке удаления заметки
$(document).on('click', '.deleteNoteButton', function() {
    var note = $(this).data('note');  // Получение значения заметки из атрибута data-note кнопки удаления
    $.post('/delete_note', {note: note}, function(data) {
        updateNotesList();  // Вызов функции обновления списка заметок на фронтенде
    });
});

// Вызов функции обновления списка заметок при загрузке страницы
$(document).ready(function() {
    updateNotesList();
});