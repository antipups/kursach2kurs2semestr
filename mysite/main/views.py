from django.http import HttpResponse
from django.shortcuts import render
# from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
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

dict_of_data = {"Buttons":
                     (('Добавить в', 'Удалить из', 'Изменить в', 'Просмотреть'),
                      tuple_with_tables,
                     ),
                "DB":
                     Pharmacy.objects.all(),
                "Mods":
                     ("Работа с базой данных (Добавление, удаление)", "Задания"),
                # "Tables":
                #      (),
                }


@csrf_exempt
def hw(request):

    dict_of_tables = {'Лекарства': Medicament,  # словарь с наименованием таблицы / объектом таблицы
                      'Аптека': Pharmacy,
                      'Фирма': Manufacturer,
                      'Партия': Lot,
                      'Страна': Country,
                      'Район': District,
                      'Рабочий': Employee,
                      'Фармакалогическая группа': Pharma_group,
                      'Форма лекарства': Shape,
                      }

    if request.method == 'POST':
        string = request.POST.get('mode')
        if string.find('смотр') > -1:
            table = dict_of_tables.get(string[string.rfind(':') + 2:])
            dict_of_data.update({
                'name_of_table': string[string.find(':'):],
                'name_of_rows': table.readable(),
                'Table': table.objects.values_list()})
            return render(request, 'tables.html', dict_of_data)
    return HttpResponse('Hello World')
