function updateMemoryUsage() {
    $.ajax({
        url: '/memory-usage',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            $('#memory_usage').text(response.memory_usage + ' GB');
            $('#total_memory').text('/ ' + response.total_memory + ' GB');
            $('#memory_percent').text('(' + response.memory_percent + '%)');
        },
        complete: function() {
            // Вызов функции снова через 1 секунду
            setTimeout(updateMemoryUsage, 1000);
        }
    });
}

// Вызов функции первый раз
$(document).ready(function() {
    updateMemoryUsage();
});