from django.shortcuts import render
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

    if request.method == 'POST':    # если юзер нажал на кнопку

        string = request.POST.get('mode')
        table = dict_of_tables.get(string[string.rfind(':') + 2:])

        if string.find('смотр') > -1:   # для кнопки посмотреть
            dict_of_data.update({
                'name_of_table': string[string.find(':'):],
                'name_of_rows': table.readable(),
                'Table': table.objects.values_list()
            })
            return render(request, 'read_table.html', dict_of_data)

        elif string.find('обави') > -1:     # для кнопки добавить
            rows = table.readable()[1:]
            ids, rows = tuple(x for x in rows if x.find('id_of_') == 0), tuple(x for x in rows if x.find('id_of_') == -1)

            dict_of_tables = {
                'Country': Country.objects.values_list(),
                'Shape': Shape.objects.values_list(),
                'Group': Pharma_group.objects.values_list(),
                'Manufact': Manufacturer.objects.values_list(),
                'District': District.objects.values_list(),
                'Pharm': Pharmacy.objects.values_list(),
                'Lot': Lot.objects.values_list(),
                'Employee': Employee.objects.values_list(),
            }

            tables = {}
            for i in enumerate(tuple(dict_of_tables.get(x[x.find('_of_') + 4:].capitalize()) for x in ids)):    # в tables помещяем внешний ключ + примари ключИ
                tables.update({ids[i[0]]: tuple(str(j[0]) + ' | ' + j[1] for j in i[1])})

            dict_of_data.update({
                'name_of_table': string[string.find(':') + 2:],
                'name_of_rows': rows,
                'ids': ids,
                'tables': tables,
            })
            return render(request, 'add_in_table.html', dict_of_data)


