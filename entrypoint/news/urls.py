from django.urls import path
from . import views

urlpatterns = [
    path('', views.newsblocks, name='news_index'),
    path('update-data/', views.update_data, name='update_data'),
    path('news/<slug:slug>/', views.detail, name='news_detail'),
]
