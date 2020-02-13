from django.urls import path
from django.views.generic import ListView, DetailView
from .models import *

tuple_with_tables = (('Лекарства',
                      'Аптека',
                      'Фирма',
                      'Партия'),
                     ('Страна',
                      'Район',
                      'Рабочий',
                      'Фармакалогическая группа',
                      'Форма лекарства',
                      ))


def lol():
    # print(Pharmacy.__str__(Pharmacy))     # вывод полей класса
    return Pharmacy.objects.all()


urlpatterns = [
    path('',
         ListView.as_view(queryset=({"Buttons":
                                         (('Добавить в', 'Удалить из', 'Изменить в'),
                                          tuple_with_tables,
                                         ),
                                     "DB":
                                         Pharmacy.objects.all(),
                                     "Mods":
                                         ("Работа с базой данных (Добавление, удаление)", "Задания"),
                                     }),
                          template_name='content.html'),
         name='hw'),
]
