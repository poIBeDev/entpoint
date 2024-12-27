import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import yfinance as yf



def get_moex_index():
    try:
        # URL для получения информации об индексе MOEX
        url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/IMOEX.json'
        response = requests.get(url)
        data = response.json()

        # Извлекаем данные из ответа
        marketdata = data.get('marketdata', {})
        marketdata_columns = marketdata.get('columns', [])
        marketdata_data = marketdata.get('data', [])

        if marketdata_data:
            # Создаем словарь {имя_колонки: значение} для первой записи
            marketdata_dict = dict(zip(marketdata_columns, marketdata_data[0]))
            # print(f"marketdata_dict: {marketdata_dict}")

            # Получаем значение CURRENTVALUE (текущая цена)
            current_value = marketdata_dict.get('CURRENTVALUE')

            # Получаем изменение за день в абсолютных значениях (LASTCHANGE)
            day_change = marketdata_dict.get('LASTCHANGE')

            # Получаем изменение за день в процентах (LASTCHANGEPRC)
            day_change_prc = marketdata_dict.get('LASTCHANGEPRC')

            # Проверяем и форматируем значения
            if current_value is not None:
                current_value = round(float(current_value), 2)
            else:
                current_value = None

            if day_change is not None:
                day_change = round(float(day_change), 2)
            else:
                day_change = None

            if day_change_prc is not None:
                day_change_prc = round(float(day_change_prc), 2)
            else:
                day_change_prc = None

            # Получаем дату и время обновления
            trade_date = marketdata_dict.get('TRADEDATE')  # "2024-10-04"
            update_time = marketdata_dict.get('TIME')      # "18:50:00"

            # Форматируем дату и время
            if trade_date and update_time:
                # Преобразуем строку в объект datetime
                datetime_str = f"{trade_date} {update_time}"
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                # Форматируем дату и время
                moex_date = datetime_obj.strftime("%d.%m.%Y %H:%M")
            else:
                moex_date = None

            # Возвращаем полученные данные
            return current_value, moex_date, day_change, day_change_prc
        else:
            print("Данные marketdata пусты.")
            return None, None, None, None

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None, None, None, None
    
def get_currency_rate(char_code):
    try:
        # Получаем XML с курсами валют
        url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        response = requests.get(url)
        response.encoding = 'windows-1251'  # Устанавливаем правильную кодировку

        # Парсим XML
        tree = ET.fromstring(response.text)

        # Находим валюту по CharCode
        for valute in tree.findall('Valute'):
            code = valute.find('CharCode').text
            if code == char_code:
                value = valute.find('Value').text.replace(',', '.')
                nominal = valute.find('Nominal').text.replace(',', '.')
                rate = round(float(value) / float(nominal), 4)
                date = tree.attrib['Date']
                return rate, date
        return None, None
    except Exception as e:
        print(f"Ошибка при получении курса валюты {char_code}: {e}")
        return None, None
    
def get_oil_price():
    try:
        oil = yf.Ticker("BZ=F")  # Тикер Brent Crude Oil
        data = oil.history(period="5d")  # Изменили период на '5d'
        if not data.empty and len(data) >= 2:
            current_price = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2]
            day_change = round(current_price - previous_close, 2)
            if previous_close != 0:
                day_change_prc = round((day_change / previous_close) * 100, 2)
            else:
                day_change_prc = None

            # Получаем дату и время обновления
            last_update = data.index[-1]
            oil_date = last_update.strftime("%d.%m.%Y %H:%M")

            return round(current_price, 2), oil_date, day_change, day_change_prc
        else:
            print("Недостаточно данных для нефти Brent.")
            return None, None, None, None
    except Exception as e:
        print(f"Ошибка при получении цены нефти: {e}")
        return None, None, None, None
    
def get_rtsi_index():
    try:
        url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/RTSI.json'
        response = requests.get(url)
        data = response.json()

        marketdata = data.get('marketdata', {})
        marketdata_columns = marketdata.get('columns', [])
        marketdata_data = marketdata.get('data', [])

        if marketdata_data:
            marketdata_dict = dict(zip(marketdata_columns, marketdata_data[0]))

            current_value = marketdata_dict.get('CURRENTVALUE')
            day_change = marketdata_dict.get('LASTCHANGE')
            day_change_prc = marketdata_dict.get('LASTCHANGEPRC')

            if current_value is not None:
                current_value = round(float(current_value), 2)
            else:
                current_value = None

            if day_change is not None:
                day_change = round(float(day_change), 2)
            else:
                day_change = None

            if day_change_prc is not None:
                day_change_prc = round(float(day_change_prc), 2)
            else:
                day_change_prc = None

            trade_date = marketdata_dict.get('TRADEDATE')
            update_time = marketdata_dict.get('TIME')

            if trade_date and update_time:
                moex_date = f"{trade_date} {update_time}"
            else:
                moex_date = None

            return current_value, moex_date, day_change, day_change_prc
        else:
            print("Данные marketdata пусты.")
            return None, None, None, None
    except Exception as e:
        print(f"Ошибка при получении данных индекса РТС: {e}")
        return None, None, None, None
    
def get_sp500_index():
    try:
        sp500 = yf.Ticker("^GSPC")
        data = sp500.history(period="5d")  # Изменили период на '5d'
        if not data.empty and len(data) >= 2:
            current_price = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2]
            day_change = round(current_price - previous_close, 2)
            if previous_close != 0:
                day_change_prc = round((day_change / previous_close) * 100, 2)
            else:
                day_change_prc = None

            # Получаем дату и время обновления
            last_update = data.index[-1]
            sp_date = last_update.strftime("%d.%m.%Y %H:%M")

            return round(current_price, 2), sp_date, day_change, day_change_prc
        else:
            print("Недостаточно данных для индекса S&P 500.")
            return None, None, None, None
    except Exception as e:
        print(f"Ошибка при получении данных индекса S&P 500: {e}")
        return None, None, None, None