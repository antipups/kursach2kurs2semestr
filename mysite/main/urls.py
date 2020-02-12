from django.urls import path
from django.views.generic import ListView, DetailView
from .models import *


urlpatterns = [
    path('',
         ListView.as_view(queryset=(('Добавить в', 'Аптеки', 'Фирмы', 'Партии'),
                                    ('Удалить из', 'аптек', 'фирм', 'партий'),
                                    ('Изменить в', 'аптеках', 'фирмах', 'партиях')),
                          template_name='content.html'),
         name='hw'),
]
