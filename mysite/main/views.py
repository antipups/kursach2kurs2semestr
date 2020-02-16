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
                }   # начальный словарь, кторый мы и будем таскать


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


@csrf_exempt
def hw(request, dict_of_tables=dict_of_tables):
    dict_of_data['win'] = ''
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
                'Pharma_group': Pharma_group.objects.values_list(),
                'Manufacturer': Manufacturer.objects.values_list(),
                'District': District.objects.values_list(),
                'Pharmacy': Pharmacy.objects.values_list(),
                'Lot': Lot.objects.values_list(),
                'Employee': Employee.objects.values_list(),
            }

            tables = {}
            if ids:
                for i in enumerate(tuple(dict_of_tables.get(x[x.find('_of_') + 4:].capitalize()) for x in ids)):    # в tables помещяем внешний ключ + примари ключИ
                    if ids[0] in ('id_of_shape', 'id_of_pharma_group', 'id_of_manufacturer', 'id_of_country', 'id_of_district'):
                        tables.update({ids[i[0]]: tuple(str(j[0]) + ' | ' + j[1] for j in i[1])})  # можно улудшить + названием, но это лень
                    elif ids[0] == 'id_of_pharmacy':
                        tables.update({ids[i[0]]: tuple(
                            str(j[0]) + ' | ' + j[2] for j in i[1])})  # можно улудшить + названием, но это лень
                    elif ids[0] == 'id_of_lot':
                        tables.update({ids[i[0]]: tuple(
                            str(j[0]) + ' | ' + j[3] for j in i[1])})  # можно улудшить + названием, но это лень
                    elif ids[0] == 'id_of_employee':
                        tables.update({ids[i[0]]: tuple(
                            str(j[0]) + ' | ' + j[1] + ' ' + j[2] + ' ' + j[3] for j in i[1])})  # можно улудшить + названием, но это лень
            dict_of_data.update({   # в инфу о гет запросе суем назву таблицы, её ряды
                'name_of_table': string[string.find(':') + 2:],
                'name_of_rows': rows,
                'ids': ids,
                'tables': tables,
            })
            return render(request, 'add_in_table.html', dict_of_data)


@csrf_exempt
def add_mode(request, dict_of_tables=dict_of_tables):
    if request.method == 'POST':
        dict_of_data.update({'win': False})
        dict_of_post = dict(request.POST)
        object_of_table = dict_of_tables.get(dict_of_data.get('name_of_table'))     # получаем таблицу в виде объекта с хтмла
        for row in dict_of_post.items():
            if row[0].find('id_of_') > -1:  # если это id то режем до id
                if (row[1][0][:row[1][0].find(' ')]).isdigit() is False:
                    return render(request, 'add_in_table.html', dict_of_data)
                dict_of_post[row[0]] = eval(row[0][row[0].find('_of_') + 4:].capitalize()).objects.get(id=int(row[1][0][:row[1][0].find(' ')]))
            else:
                dict_of_post[row[0]] = row[1][0]
        try:
            object_of_table.objects.create(**dict_of_post)
        except ValueError:
            return render(request, 'add_in_table.html', dict_of_data)
        dict_of_data.update({'win': True})

        return render(request, 'add_in_table.html', dict_of_data)
