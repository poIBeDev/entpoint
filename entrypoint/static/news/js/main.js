function updateData() {
    var updateDataUrl = "{% url 'update_data' %}";
    var upIconUrl = "{% static 'news/assets/courses-and-schedules/up.svg' %}";
    var downIconUrl = "{% static 'news/assets/courses-and-schedules/down.svg' %}";

    console.log('Начало обновления данных'); // Отладочное сообщение
    $.ajax({
        url: updateDataUrl,  // Используем переменную, заданную в шаблоне
        type: 'GET',
        success: function(data) {
            console.log('Получены данные:', data); // Отладочное сообщение

            // MOEX
            $('#moex_price').text(data.moex_price || '-');
            $('#moex_date').text(data.moex_date || '-');
            if (data.moex_day_change > 0) {
                $('#moex_change_icon').attr('src', upIconUrl);
                $('#moex_day_change').text('+' + data.moex_day_change_prc + '%').removeClass().addClass('positive');
            } else if (data.moex_day_change < 0) {
                $('#moex_change_icon').attr('src', downIconUrl);
                $('#moex_day_change').text(data.moex_day_change_prc + '%').removeClass().addClass('negative');
            } else {
                $('#moex_change_icon').attr('src', '');
                $('#moex_day_change').text('0%').removeClass().addClass('neutral');
            }

            // Brent
            $('#oil_price').text(data.oil_price || '-');
            $('#oil_date').text(data.oil_date || '-');
            if (data.oil_day_change > 0) {
                $('#oil_change_icon').attr('src', upIconUrl);
                $('#oil_day_change').text('+' + data.oil_day_change_prc + '%').removeClass().addClass('positive');
            } else if (data.oil_day_change < 0) {
                $('#oil_change_icon').attr('src', downIconUrl);
                $('#oil_day_change').text(data.oil_day_change_prc + '%').removeClass().addClass('negative');
            } else {
                $('#oil_change_icon').attr('src', '');
                $('#oil_day_change').text('0%').removeClass().addClass('neutral');
            }

            // RTSI
            $('#rtsi_price').text(data.rtsi_price || '-');
            $('#rtsi_date').text(data.rtsi_date || '-');
            if (data.rtsi_day_change > 0) {
                $('#rtsi_change_icon').attr('src', upIconUrl);
                $('#rtsi_day_change').text('+' + data.rtsi_day_change_prc + '%').removeClass().addClass('positive');
            } else if (data.rtsi_day_change < 0) {
                $('#rtsi_change_icon').attr('src', downIconUrl);
                $('#rtsi_day_change').text(data.rtsi_day_change_prc + '%').removeClass().addClass('negative');
            } else {
                $('#rtsi_change_icon').attr('src', '');
                $('#rtsi_day_change').text('0%').removeClass().addClass('neutral');
            }

            // S&P 500
            $('#sp500_price').text(data.sp500_price || '-');
            $('#sp500_date').text(data.sp500_date || '-');
            if (data.sp500_day_change > 0) {
                $('#sp500_change_icon').attr('src', upIconUrl);
                $('#sp500_day_change').text('+' + data.sp500_day_change_prc + '%').removeClass().addClass('positive');
            } else if (data.sp500_day_change < 0) {
                $('#sp500_change_icon').attr('src', downIconUrl);
                $('#sp500_day_change').text(data.sp500_day_change_prc + '%').removeClass().addClass('negative');
            } else {
                $('#sp500_change_icon').attr('src', '');
                $('#sp500_day_change').text('0%').removeClass().addClass('neutral');
            }

            // Валюты
            // USD/RUB
            $('#usd_rate').text(data.usd_rate || '-');
            $('#usd_date').text(data.currency_date || '-');

            // EUR/RUB
            $('#eur_rate').text(data.eur_rate || '-');

            // CNY/RUB
            $('#cny_rate').text(data.cny_rate || '-');
        },
        error: function(error) {
            console.error('Ошибка обновления данных:', error);
        }
    });
}

// Обновляем данные каждые 30 секунд
setInterval(updateData, 30000);

// Первоначальный вызов для мгновенного обновления при загрузке страницы
updateData();