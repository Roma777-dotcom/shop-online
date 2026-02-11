// Кастомный JavaScript для админки

$(document).ready(function() {
    // Добавляем всплывающие подсказки
    $('[title]').tooltip();
    
    // Подсветка строк таблицы при наведении
    $('table tbody tr').hover(
        function() {
            $(this).addClass('table-active');
        },
        function() {
            $(this).removeClass('table-active');
        }
    );
    
    // Быстрое редактирование количества товара
    $('.quick-edit').click(function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        var newQuantity = prompt('Введите новое количество:', $(this).data('quantity'));
        
        if (newQuantity !== null) {
            $.ajax({
                url: '/admin/quick-edit/',
                method: 'POST',
                data: {
                    product_id: productId,
                    quantity: newQuantity,
                    csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    location.reload();
                }
            });
        }
    });
    
    // Экспорт данных
    $('.export-btn').click(function(e) {
        e.preventDefault();
        var format = $(this).data('format');
        window.location.href = '/admin/export/?format=' + format;
    });
});

// Функция для обновления цены
function updatePrice(productId, newPrice) {
    if (confirm('Вы уверены, что хотите изменить цену?')) {
        $.ajax({
            url: '/admin/update-price/',
            method: 'POST',
            data: {
                product_id: productId,
                price: newPrice,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                alert('Цена успешно обновлена!');
                location.reload();
            }
        });
    }
}