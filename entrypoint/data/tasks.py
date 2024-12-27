# data/tasks.py
from django.core.cache import cache
from celery import shared_task
from .utils import (
    get_moex_index,
    get_currency_rate,
    get_oil_price,
    get_rtsi_index,
    get_sp500_index,
)

import logging

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

@shared_task
def update_moex():
    price, date_str, day_change, day_change_prc = get_moex_index()
    if price is not None and date_str is not None:
        # Успешное обновление данных, обновляем кэш
        cache.set('MOEX', {
            'price': price,
            'date': date_str,
            'day_change': day_change,
            'day_change_prc': day_change_prc,
        }, timeout=60)  # Обновляем данные каждые 60 секунд
    else:
        # Если данные не обновились, оставляем старые
        cached_moex = cache.get('MOEX')
        if cached_moex:
            logger.warning("Не удалось обновить данные для MOEX, оставляем старые значения.")
        else:
            logger.warning("Не удалось получить новые данные для MOEX, и в кэше ничего нет.")

@shared_task
def update_currencies():
    for code in ['USD', 'EUR', 'CNY']:
        rate, date_str = get_currency_rate(code)
        if rate is not None and date_str is not None:
            cache.set(f'{code}/RUB', {
                'price': rate,
                'date': date_str,
            }, timeout=21600)  # Обновляем данные каждые 6 часов
        else:
            cached_currency = cache.get(f'{code}/RUB')
            if cached_currency:
                logger.warning(f"Не удалось обновить данные для {code}/RUB, оставляем старые значения.")
            else:
                logger.warning(f"Не удалось получить новые данные для {code}/RUB, и в кэше ничего нет.")

@shared_task
def update_oil():
    price, date_str, day_change, day_change_prc = get_oil_price()
    if price is not None and date_str is not None:
        cache.set('Brent', {
            'price': round(price, 3),  # Обрезаем до 3 знаков после запятой
            'date': date_str,
            'day_change': day_change,
            'day_change_prc': day_change_prc,
        }, timeout=60)  # Обновляем данные каждые 60 секунд
    else:
        cached_oil = cache.get('Brent')
        if cached_oil:
            logger.warning("Не удалось обновить данные для Brent, оставляем старые значения.")
        else:
            logger.warning("Не удалось получить новые данные для Brent, и в кэше ничего нет.")

@shared_task
def update_rtsi():
    price, date_str, day_change, day_change_prc = get_rtsi_index()
    if price is not None and date_str is not None:
        cache.set('RTSI', {
            'price': price,
            'date': date_str,
            'day_change': day_change,
            'day_change_prc': day_change_prc,
        }, timeout=60)  # Обновляем данные каждые 60 секунд
    else:
        cached_rtsi = cache.get('RTSI')
        if cached_rtsi:
            logger.warning("Не удалось обновить данные для RTSI, оставляем старые значения.")
        else:
            logger.warning("Не удалось получить новые данные для RTSI, и в кэше ничего нет.")

@shared_task
def update_sp500():
    price, date_str, day_change, day_change_prc = get_sp500_index()
    if price is not None and date_str is not None:
        cache.set('S&P 500', {
            'price': price,
            'date': date_str,
            'day_change': day_change,
            'day_change_prc': day_change_prc,
        }, timeout=60)  # Обновляем данные каждые 60 секунд
    else:
        cached_sp500 = cache.get('S&P 500')
        if cached_sp500:
            logger.warning("Не удалось обновить данные для S&P 500, оставляем старые значения.")
        else:
            logger.warning("Не удалось получить новые данные для S&P 500, и в кэше ничего нет.")
