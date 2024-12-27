from django.shortcuts import render
from django.core.cache import cache
import logging
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import News
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)

def index_news(request):
    return render(request, 'news/news.html')

def index(request):
    # Получаем данные из кэша
    moex = cache.get('MOEX')
    usd = cache.get('USD/RUB')
    eur = cache.get('EUR/RUB')
    cny = cache.get('CNY/RUB')
    oil = cache.get('Brent')
    rtsi = cache.get('RTSI')
    sp500 = cache.get('S&P 500')

    # MOEX
    moex_price = moex['price'] if moex else None
    moex_date = moex['date'] if moex else None
    if moex_date:
        moex_date = datetime.strptime(moex_date, "%d.%m.%Y %H:%M").strftime("%d.%m.%Y")
    moex_day_change = moex['day_change'] if moex else None
    moex_day_change_prc = moex['day_change_prc'] if moex else None

    # Валюты
    usd_rate = usd['price'] if usd else None
    eur_rate = eur['price'] if eur else None
    cny_rate = cny['price'] if cny else None
    currency_date = usd['date'] if usd else None  # Предполагаем, что дата у всех валют одинаковая
    if currency_date:
        currency_date = datetime.strptime(currency_date, "%d.%m.%Y").strftime("%d.%m.%Y")

    # Нефть Brent
    oil_price = oil['price'] if oil else None
    if oil_price is not None:
        oil_price = round(oil_price, 3)  # Округляем до 3 знаков после запятой
    oil_date = oil['date'] if oil else None
    if oil_date:
        oil_date = datetime.strptime(oil_date, "%d.%m.%Y %H:%M").strftime("%d.%m.%Y")
    oil_day_change = oil['day_change'] if oil else None
    oil_day_change_prc = oil['day_change_prc'] if oil else None

    # RTSI
    rtsi_price = rtsi['price'] if rtsi else None
    rtsi_date = rtsi['date'] if rtsi else None
    if rtsi_date:
        rtsi_date = datetime.strptime(rtsi_date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
    rtsi_day_change = rtsi['day_change'] if rtsi else None
    rtsi_day_change_prc = rtsi['day_change_prc'] if rtsi else None

    # S&P 500
    sp500_price = sp500['price'] if sp500 else None
    sp500_date = sp500['date'] if sp500 else None
    if sp500_date:
        sp500_date = datetime.strptime(sp500_date, "%d.%m.%Y %H:%M").strftime("%d.%m.%Y")
    sp500_day_change = sp500['day_change'] if sp500 else None
    sp500_day_change_prc = sp500['day_change_prc'] if sp500 else None

    # Формируем словарь context
    context = {
        # MOEX
        'moex_price': moex_price,
        'moex_date': moex_date,
        'moex_day_change': moex_day_change,
        'moex_day_change_prc': moex_day_change_prc,

        # Валюты
        'usd_rate': usd_rate,
        'eur_rate': eur_rate,
        'cny_rate': cny_rate,
        'currency_date': currency_date,

        # Нефть Brent
        'oil_price': oil_price,
        'oil_date': oil_date,
        'oil_day_change': oil_day_change,
        'oil_day_change_prc': oil_day_change_prc,

        # RTSI
        'rtsi_price': rtsi_price,
        'rtsi_date': rtsi_date,
        'rtsi_day_change': rtsi_day_change,
        'rtsi_day_change_prc': rtsi_day_change_prc,

        # S&P 500
        'sp500_price': sp500_price,
        'sp500_date': sp500_date,
        'sp500_day_change': sp500_day_change,
        'sp500_day_change_prc': sp500_day_change_prc,
    }

    return render(request, 'news/layout.html', context)

def update_data(request):
    # Получаем данные из кэша
    moex = cache.get('MOEX')
    oil = cache.get('Brent')
    rtsi = cache.get('RTSI')
    sp500 = cache.get('S&P 500')
    usd = cache.get('USD/RUB')
    eur = cache.get('EUR/RUB')
    cny = cache.get('CNY/RUB')

    # MOEX
    moex_price = moex['price'] if moex else None
    moex_date = moex['date'] if moex else None
    if moex_date:
        moex_date = datetime.strptime(moex_date, "%d.%m.%Y %H:%M").strftime("%d.%m.%Y")
    moex_day_change = moex['day_change'] if moex else None
    moex_day_change_prc = moex['day_change_prc'] if moex else None

    # Валюты
    usd_rate = usd['price'] if usd else None
    eur_rate = eur['price'] if eur else None
    cny_rate = cny['price'] if cny else None
    currency_date = usd['date'] if usd else None  # Предполагаем, что дата у всех валют одинаковая
    if currency_date:
        currency_date = datetime.strptime(currency_date, "%d.%m.%Y").strftime("%d.%m.%Y")

    # Нефть Brent
    oil_price = oil['price'] if oil else None
    if oil_price is not None:
        oil_price = round(oil_price, 3)  # Округляем до 3 знаков после запятой
    oil_date = oil['date'] if oil else None
    if oil_date:
        oil_date = datetime.strptime(oil_date, "%d.%m.%Y %H:%M").strftime("%d.%m.%Y")
    oil_day_change = oil['day_change'] if oil else None
    oil_day_change_prc = oil['day_change_prc'] if oil else None

    # RTSI
    rtsi_price = rtsi['price'] if rtsi else None
    rtsi_date = rtsi['date'] if rtsi else None
    if rtsi_date:
        rtsi_date = datetime.strptime(rtsi_date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
    rtsi_day_change = rtsi['day_change'] if rtsi else None
    rtsi_day_change_prc = rtsi['day_change_prc'] if rtsi else None

    # S&P 500
    sp500_price = sp500['price'] if sp500 else None
    sp500_date = sp500['date'] if sp500 else None
    if sp500_date:
        sp500_date = datetime.strptime(sp500_date, "%d.%m.%Y %H:%M").strftime("%d.%m.%Y")
    sp500_day_change = sp500['day_change'] if sp500 else None
    sp500_day_change_prc = sp500['day_change_prc'] if sp500 else None

    # Формируем JSON ответ с данными
    data = {
    # MOEX
    'moex_price': moex_price,
    'moex_date': moex_date,
    'moex_day_change': moex_day_change,
    'moex_day_change_prc': moex_day_change_prc,

    # Brent
    'oil_price': oil_price,
    'oil_date': oil_date,
    'oil_day_change': oil_day_change,
    'oil_day_change_prc': oil_day_change_prc,

    # RTSI
    'rtsi_price': rtsi_price,
    'rtsi_date': rtsi_date,
    'rtsi_day_change': rtsi_day_change,
    'rtsi_day_change_prc': rtsi_day_change_prc,

    # S&P 500
    'sp500_price': sp500_price,
    'sp500_date': sp500_date,
    'sp500_day_change': sp500_day_change,
    'sp500_day_change_prc': sp500_day_change_prc,

    # Валюты
    'usd_rate': usd_rate,
    'eur_rate': eur_rate,
    'cny_rate': cny_rate,
    'currency_date': currency_date,
}

    return JsonResponse(data)


def newsblocks(request):
    # Получаем все новости, отсортированные по времени в порядке убывания
    news_list = News.objects.order_by('-timestamp')
    
    # Настраиваем пагинацию: 20 новостей на страницу
    paginator = Paginator(news_list, 25)
    
    # Получаем номер текущей страницы из GET-параметра 'page'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for news_item in page_obj:
        time_diff = timezone.now() - news_item.timestamp
        news_item.is_recent = time_diff < timedelta(hours=1)
    
    # Передаем объект страницы в шаблон
    return render(request, 'news/news.html', {'page_obj': page_obj, 'current_section': 'news'})

def detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    return render(request, 'news/detail.html', {'news_item': news_item})