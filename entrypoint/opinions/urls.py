from django.urls import path
from . import views

urlpatterns = [
    path('', views.opinions_list, name='opinions_list'),
    path('<slug:slug>/', views.opinion_detail, name='opinion_detail'),
]