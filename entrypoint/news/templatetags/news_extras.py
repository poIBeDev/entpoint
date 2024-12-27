from django import template
from django.utils import timezone
import datetime
import re
from django.utils.safestring import mark_safe
from razdel import sentenize

register = template.Library()

@register.filter
def first_sentences(value, count=2):
    # Разбиваем текст на предложения
    sentences = re.split(r'(?<=[.!?]) +', value)
    # Возвращаем первые 'count' предложений
    return ' '.join(sentences[:count])

@register.filter
def remove_first_sentence(value):
    sentences = re.split(r'(?<=[.!?]) +', value)
    return ' '.join(sentences[1:])

@register.filter
def sentences_range(value, arg):
    # arg ожидается в формате 'start,end', где end может быть опущен
    try:
        parts = arg.split(',')
        start = int(parts[0]) - 1  # Начальный индекс (минус 1, так как индексация с нуля)
        end = int(parts[1]) if len(parts) > 1 and parts[1] else None
        sentences = re.split(r'(?<=[.!?]) +', value)
        return ' '.join(sentences[start:end])
    except (ValueError, TypeError, IndexError):
        return ''
    
@register.filter
def split_tickers(value):
    if value and isinstance(value, str):
        # Разделяем строку по запятым и удаляем пробелы
        return [ticker.strip() for ticker in value.split(',')]
    else:
        return []

@register.filter
def time_since(value):
    now = timezone.now()
    diff = now - value

    if diff.days >= 365:
        years = diff.days // 365
        return f"{years} год(а/лет) назад"
    elif diff.days >= 30:
        months = diff.days // 30
        return f"{months} месяц(а/ев) назад"
    elif diff.days >= 1:
        return f"{diff.days} день(дней) назад"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} час(а/ов) назад"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} минут(а) назад"
    else:
        return "только что"
    

@register.filter
def auto_paragraphs_razdel(value, sentences_per_paragraph=3):
    if not value:
        return ''
    # Разбиваем текст на предложения с помощью razdel
    sentences = [sent.text for sent in sentenize(value.strip())]
    paragraphs = []
    # Группируем предложения в абзацы
    for i in range(0, len(sentences), sentences_per_paragraph):
        paragraph = ' '.join(sentences[i:i+sentences_per_paragraph])
        paragraphs.append(f'<p>{paragraph}</p>')
    result = ''.join(paragraphs)
    return mark_safe(result)