from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *


tuple_with_tables = (('Лекарства',  # кортеж со всеми таблицами
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
                "mode": '',
                'addon': False,
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
    dict_of_data['win'], dict_of_data['addon'] = '', False
    if request.method == 'POST':    # если юзер нажал на кнопку

        string = request.POST.get('mode')   # получаем с страницы вс. нужную информацию
        table = dict_of_tables.get(string[string.rfind(':') + 2:])
        if string.find('смотр') > -1:   # для кнопки посмотреть
            dict_of_data.update({
                'name_of_table': string[string.find(':'):],
                'name_of_rows': table.readable(),
                'Table': table.objects.values_list()
            })
            return render(request, 'read_table.html', dict_of_data)

        rows = table.readable()[1:]     # получаем поля таблицы , для этого в классе каждой таблицы прописанны поля
        ids, rows = tuple(x for x in rows if x.find('id_of_') == 0), tuple(x for x in rows if x.find('id_of_') == -1)
        # выше на одну строку генерируем два кортежа, один из айдишников, то есть внешних ключей, другой из простых полей

        dict_of_tables = {      # кортеж для получения значений со всех таблиц
            'Country': Country.objects.values_list(),
            'Shape': Shape.objects.values_list(),
            'Pharma_group': Pharma_group.objects.values_list(),
            'Manufacturer': Manufacturer.objects.values_list(),
            'District': District.objects.values_list(),
            'Pharmacy': Pharmacy.objects.values_list(),
            'Lot': Lot.objects.values_list(),
            'Employee': Employee.objects.values_list(),
        }

        tables = {}     # словарь для вывода на html выдвигающихся полей

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

        dict_of_data.update({   # в инфу о гет запросе суем назву таблицы, её ряды, внешние id, ключи с внешних таблиц, и мод, в котором пашем, добавить или удалить
            'name_of_table': string[string.find(':') + 2:],
            'name_of_rows': rows,
            'ids': ids,
            'tables': tables,
            'mode': string[:string.find(':')]
        })
        if string.find('Добавить') > -1:
            return render(request, 'add_in_table.html', dict_of_data)
        elif string.find('Удалить') > -1:  # для кнопки добавить
            return render(request, 'remove_from_table.html', dict_of_data)
        elif string.find('Изменить') > -1:  # для кнопки добавить
            return render(request, 'update_table.html', dict_of_data)


@csrf_exempt
def mode(request, dict_of_tables=dict_of_tables):
    if request.method == 'POST':
        dict_of_data.update({'win': False})     # переменная для утверждения, удачная ли была операция или нет
        dict_of_post = dict(request.POST)
        object_of_table = dict_of_tables.get(dict_of_data.get('name_of_table'))     # получаем таблицу в виде объекта с хтмла
        for row in dict_of_post.items():    # получаем из html файла данные, они подаеются в словаре в виде списков, перебираем всё, и получаем чистые данные
            if row[0].find('id_of_') > -1:  # если это id то режем до id
                if (row[1][0][:row[1][0].find(' ')]).isdigit() is False:
                    return render(request, 'add_in_table.html', dict_of_data)
                dict_of_post[row[0]] = eval(row[0][row[0].find('_of_') + 4:].capitalize()).objects.get(id=int(row[1][0][:row[1][0].find(' ')]))
            else:
                dict_of_post[row[0]] = row[1][0]

        if dict_of_data.get('mode').find('Добав') > -1:   # если добавляем, то делаем добавление > проверки на наличие данных -> добавление
            try:
                object_of_table.objects.create(**dict_of_post)
            except ValueError:
                return render(request, 'add_in_table.html', dict_of_data)
            dict_of_data.update({'win': True})
            return render(request, 'add_in_table.html', dict_of_data)

        elif dict_of_data.get('mode').find('Удал') > -1:  # если делаем удаление > проверки на наличие данных -> удаление
            amount_of_remove = object_of_table.objects.filter(**dict_of_post).delete()[0]  # количество удалимых записей
            if amount_of_remove == 0:
                dict_of_data.update({'win': False})
            else:
                dict_of_data.update({'win': True, 'amount_of_remove': '3'})
            return render(request, 'remove_from_table.html', dict_of_data)

        elif dict_of_data.get('mode').find('Изме') > -1 and dict_of_data.get('addon') == False:  # если делаем обновление данных > проверка на наличие данных -> след шаг обновления
            print('Первый блок')
            try:
                object_of_table.objects.get(**dict_of_post)
                dict_of_data.update({'win': True, 'addon': True,
                                     'dict_of_post': dict_of_post})
                return render(request, 'update_table.html', dict_of_data)
            except:
                dict_of_data.update({'win': False, 'addon': False})
                return render(request, 'update_table.html', dict_of_data)

        else:
            try:
                amount_of_update = object_of_table.objects.filter(**dict_of_data.get('dict_of_post')).update(**dict_of_post)
                if amount_of_update > 0:
                    dict_of_data.update({'win': True, 'addon': False})
                else:
                    dict_of_data.update({'win': False, 'addon': False})
                return render(request, 'update_table.html', dict_of_data)
            except:
                dict_of_data.update({'win': False, 'addon': False})
                return render(request, 'update_table.html', dict_of_data)

