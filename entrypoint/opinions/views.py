from django.shortcuts import render, get_object_or_404
from .models import Opinion
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone

def opinions_list(request):
    opinions_list = Opinion.objects.order_by('-timestamp')
    paginator = Paginator(opinions_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for opinion in page_obj:
        time_diff = timezone.now() - opinion.timestamp
        opinion.is_recent = time_diff < timedelta(hours=1)

    return render(request, 'opinions/opinions_list.html', {'page_obj': page_obj, 'current_section': 'opinions'})

def opinion_detail(request, slug):
    opinion_item = get_object_or_404(Opinion, slug=slug)
    return render(request, 'opinions/opinion_detail.html', {'opinion_item': opinion_item})