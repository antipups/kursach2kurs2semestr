import pprint
from django.shortcuts import render
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from . import checker
from .models import *
from random import choice   # для спама
from string import ascii_uppercase    # для спама


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
                     (('Добавить в', 'Удалить из', 'Изменить в', 'Просмотреть', 'Поиск'),
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
        string = request.POST.get('mode')
        table = dict_of_tables.get(string[string.rfind(':') + 2:])
        name_of_table_on_engl = str(table)
        if string.find('смотр') > -1:   # для кнопки посмотреть
            dict_of_data.update({
                'name_of_table': string[string.find(':'):],
                'name_of_rows': table.readable_rus(),
                'Table': tuple(map(lambda row: row.getter, table.objects.all()))
            })
            return render(request, 'read_table.html', dict_of_data)

        engl_rows = rows = table.readable()[1:]     # получаем поля таблицы , для этого в классе каждой таблицы прописанны поля
        rus_rows = table.readable_rus()[1:]
        dict_of_data.update({'data_for_find': table.readable()})

        ids, rows, code = tuple(x for x in rows if x.find('id_of_') == 0), tuple(x for x in rows if x.find('id_of_') == -1 and x.find('code') == -1), tuple(x for x in rows if x.find('code') > -1)
        engl_ids = tuple(ids)
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


        rows, ids, code = [], [], []

        for index, value in enumerate(engl_rows):
            if value.find('id_of_') > -1:
                ids.append(rus_rows[index])
            elif value.find('id_of_') == -1 and value.find('code') == -1:
                rows.append(rus_rows[index])
            else:
                code.append(rus_rows[index])

        dict_ids = {}       # создаем словарь с русским ключем и английский значением, чтоб сортировать их на айди и
        for id_ in range(len(ids)):
            dict_ids.update({ids[id_]:engl_ids[id_]})

        dict_rows = {}  # эквивалент верхнему
        for row_ in range(len(engl_rows)):
            if engl_rows[row_].find('id_of_') == -1 and engl_rows[row_].find('code') == -1:
                dict_rows.update({rus_rows[row_]: engl_rows[row_]})


        dict_of_data.update({   # в инфу о гет запросе суем назву таблицы, её ряды, внешние id, ключи с внешних таблиц, и мод, в котором пашем, добавить или удалить
            'name_of_table': string[string.find(':') + 2:],
            'name_of_rows': dict_rows,
            'code': code,
            'ids': dict_ids,
            'tables': tables,
            'mode': string[:string.find(':')],
            'model': name_of_table_on_engl[name_of_table_on_engl.rfind('.') + 1:name_of_table_on_engl.rfind("'")].lower()
        })

        if string.find('Поиск') > -1:
            dict_of_data.update({'template': 'find_in_table.html'})
            return render(request, 'find_in_table.html', dict_of_data)
        if string.find('Добавить') > -1:
            dict_of_data.update({'template': 'add_in_table.html'})
            return render(request, 'add_in_table.html', dict_of_data)
        elif string.find('Удалить') > -1:  # для кнопки добавить
            dict_of_data.update({'template': 'remove_from_table.html'})
            return render(request, 'remove_from_table.html', dict_of_data)
        elif string.find('Изменить') > -1:  # для кнопки добавить
            dict_of_data.update({'template': 'update_table.html'})
            return render(request, 'update_table.html', dict_of_data)
        elif string.find('Поиск') > -1:  # для кнопки добавить
            dict_of_data.update({'template': 'find_in_table.html'})
            return render(request, 'find_in_table.html', dict_of_data)


@csrf_exempt
def mode(request, dict_of_tables=dict_of_tables):
    if request.method == 'POST':
        dict_of_data.update({'win': False})     # переменная для утверждения, удачная ли была операция или нет
        dict_of_post = dict(request.POST)
        list_to_del = []    # список в который поместятся все ключи которые имеют пустые значения
        object_of_table = dict_of_tables.get(dict_of_data.get('name_of_table'))     # получаем таблицу в виде объекта с хтмла
        for row in dict_of_post.items():    # получаем из html файла данные, они подаеются в словаре в виде списков, перебираем всё, и получаем чистые данные
            if row[0].find('id_of_') > -1:  # если это id то режем до id
                if (row[1][0][:row[1][0].find(' ')]).isdigit() is False and dict_of_data.get('mode').find('Поиск') == -1:
                    return render(request, 'add_in_table.html', dict_of_data)
                if dict_of_data.get('mode').find('Поиск') > -1 and row[1][0][:row[1][0].find(' ')].isdigit() is False:  # если режим поиска - все аргументы НЕ обязательны
                    list_to_del.append(row[0])
                else:
                    dict_of_post[row[0]] = eval(row[0][row[0].find('_of_') + 4:].capitalize()).objects.get(id=int(row[1][0][:row[1][0].find(' ')]))
            else:
                if dict_of_data.get('mode').find('Поиск') > -1 and not row[1][0]:
                    list_to_del.append(row[0])
                else:
                    dict_of_post[row[0]] = row[1][0]

        for remove_element in list_to_del:  # чистим данные от пользователя, а именно все данные которые он не заполнил
            del dict_of_post[remove_element]

        try:
            html = dict_of_data.get('template')
            if dict_of_data.get('mode').find('Поиск') != 0 and eval('checker.' + dict_of_data.get('model') + '(**dict_of_post)') is not True:   # проверка на данные
                raise ValueError

            if dict_of_data.get('mode').find('Поиск') > -1:
                result_of_search = object_of_table.objects.filter(**dict_of_post).values_list()
                if result_of_search:
                    dict_of_data.update({'win': True, 'data_of_object': result_of_search})

            elif dict_of_data.get('mode').find('Добав') > -1:   # если добавляем, то делаем добавление > проверки на наличие данных -> добавление
                if dict_of_post.get('title_of_country') is not None:    # для таблицы с странами (там должен быть капс)
                    dict_of_post['title_of_country'] = dict_of_post.get('title_of_country').upper()
                object_of_table.objects.create(**dict_of_post)

            elif dict_of_data.get('mode').find('Удал') > -1:  # если делаем удаление > проверки на наличие данных -> удаление
                amount_of_remove = object_of_table.objects.filter(**dict_of_post).delete()[0]  # количество удалимых записей
                if amount_of_remove != 0:
                    dict_of_data.update({'amount_of_remove': amount_of_remove})

            elif dict_of_data.get('mode').find('Изме') > -1 and dict_of_data.get('addon') is False:  # если делаем обновление данных > проверка на наличие данных -> след шаг обновления
                if len(object_of_table.objects.filter(**dict_of_post)) == 0:
                    raise ValueError
                dict_of_data.update({'addon': True, 'dict_of_post': dict_of_post})

            elif dict_of_data.get('mode').find('Изме') > -1 and dict_of_data.get('addon') is True:
                amount_of_update = object_of_table.objects.filter(**dict_of_data.get('dict_of_post')).update(**dict_of_post)
                if amount_of_update > 0:
                    dict_of_data.update({'win': True, 'addon': False})
                else:
                    dict_of_data.update({'win': False, 'addon': False})

        except ValueError:
            dict_of_data.update({'cause': 'Неверно заполненны поля.', 'win': False, 'addon': False})
            return render(request, html, dict_of_data)
        except IntegrityError:
            dict_of_data.update({'cause': 'Такая запись в базе данных уже есть.', 'win': False, 'addon': False})
            return render(request, html, dict_of_data)
        else:
            dict_of_data.update({'win': True})
            return render(request, html, dict_of_data)


        # dict_of_data.update({'win': False, 'addon': False})       # НА АПДЕЙТ, ТЕСТИИИИИИ

        # dict_of_data.update({'win': False, 'addon': False})       # проверить на работу
