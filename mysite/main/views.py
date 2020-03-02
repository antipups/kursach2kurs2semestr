import pprint
from django.shortcuts import render
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context
from . import graphics
from .models import *
import util


tuple_with_tables = (('Лекарства',  # кортеж со всеми таблицами
                      'Аптека',
                      'Фирма',
                      'Партия'),
                     ('Страна',
                      'Район',
                      'Рабочий',
                      'Фармакалогическая группа',
                      'Форма лекарства',
                      'Название лекарства',
                      'Тип собственности',
                      ))

dict_of_data = {"Buttons":
                    (
                        ('Добавить в', 'Удалить из', 'Изменить в', 'Просмотреть', 'Поиск'),
                        tuple_with_tables,
                    ),
                "Buttons_for_task": ('Задание №1', 'Задание №2', 'Задание №3'),
                "mode": '',
                'addon': False,
                'pagination': False,
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
                  'Название лекарства': Name_of_medicament,
                  'Тип собственности': Type,
                  }


def task1(request):    # для задания №1
    ids = {'Аптека': tuple(),
           'Район': tuple()}    # айдишники страны и аптек
    for pharmacy in Manufacturer.objects.raw('SELECT * FROM main_pharmacy'):
        ids['Аптека'] = ids.get('Аптека') + (pharmacy.title_of_pharmacy,)
    for district in Manufacturer.objects.raw('SELECT * FROM main_district'):
        ids['Район'] = ids.get('Район') + (district.title_of_district,)
    dict_of_data.update({'ids': ids})
    return render(request, 'task1.html', dict_of_data)


@csrf_exempt
def task1_cont(request):
    dict_of_post = request.POST
    if dict_of_post.get('Аптека'):
        result = util.get_all_medicament_from_pharmacy(dict_of_post.get('Аптека'))
    elif dict_of_post.get('Район'):
        result = util.get_all_medicament_from_district(dict_of_post.get('Район'))
    else:
        dict_of_data.update({'win': "0"})
        return render(request, 'task1.html', dict_of_data)

    if result:
        dict_of_data.update({'win': True,
                             'medicaments': result,
                             'graphic1d': graphics.first_graphic(),
                             'graphic2d': graphics.second_graphic(),
                             'graphic3d': graphics.third_graphic()})
    else:
        dict_of_data.update({'win': False})
    return render(request, 'task1.html', dict_of_data)


def task2(request):  # для задания №2
    ids = {'Район': tuple()}  # айдишники страны и аптек
    for district in Manufacturer.objects.raw('SELECT * FROM main_district'):
        ids['Район'] = ids.get('Район') + (district.title_of_district,)
    dict_of_data.update({'ids': ids})
    return render(request, 'task2.html', dict_of_data)


@csrf_exempt
def task2_cont(request):
    dict_of_post = request.POST
    if dict_of_post.get('Район'):
        result = util.get_all_pharmacy_from_district(dict_of_post.get('Район'))
    else:
        dict_of_data.update({'win': "0"})
        return render(request, 'task2.html', dict_of_data)
    if result:
        dict_of_data.update({'win': True,
                             'amount_of_pharmacy': result})
    else:
        dict_of_data.update({'win': False})
    return render(request, 'task2.html', dict_of_data)


def task3(request):  # для задания №3    ВОООООБЩЕ НЕ ДЕЛАЛ, ПЕРЕШЕЛ НА ПАГИНАЦИЮ
    ids = {'Фирма': tuple()}  # айдишники страны и аптек
    for manufacturer in Manufacturer.objects.raw('SELECT * FROM main_manufacturer'):
        ids['Фирма'] = ids.get('Фирма') + (manufacturer.title_of_manufacturer,)
    dict_of_data.update({'ids': ids})
    return render(request, 'task3.html', dict_of_data)


@csrf_exempt
def task3_cont(request):
    dict_of_post = request.POST
    if dict_of_post.get('Фирма'):
        result = util.get_all_comebacks_from_manufacturer(dict_of_post.get('Фирма'))
    else:
        dict_of_data.update({'win': "0"})
        return render(request, 'task3.html', dict_of_data)
    if result:
        dict_of_data.update({'win': True,
                             'result': result[0]})
    else:
        dict_of_data.update({'win': False})
    return render(request, 'task3.html', dict_of_data)


@csrf_exempt
def hw(request, dict_of_tables=dict_of_tables):
    # print(request.POST)
    dict_of_data['win'], dict_of_data['addon'], dict_of_data['pagination'] = '', False, False
    if request.method == 'POST':    # если юзер нажал на кнопку
        string = request.POST.get('mode')
        if string.find('Задание №1') > -1:
            return task1(request)
        elif string.find('Задание №2') > -1:
            return task2(request)
        elif string.find('Задание №3') > -1:
            return task3(request)
        table = dict_of_tables.get(string[string.rfind(':') + 2:])
        dict_of_data.update({'img': 'image/' + string[string.find(':') + 2:] + '.jpg'})
        name_of_table_on_engl = str(table)
        if string.find('смотр') > -1:   # для кнопки посмотреть
            if dict_of_data.get('pages_on_' + string[string.rfind(' ') + 1:]) is None:   # добавляем некий флажок для страниц
                for key in dict_of_data.keys():     # находим старые страницы и удаляем их
                    if key.find('pages_on') > -1:
                        del dict_of_data[key]
                        break
                all_rows = tuple(map(lambda row: row.getter, table.objects.all()))
                if len(all_rows) > 10:
                    dict_of_data.update({'pages_on_' + string[string.rfind(' ') + 1:]: 1,
                                         'pagination': True,
                                         'all_rows': all_rows})
                    dict_of_data.update({'Table': all_rows[dict_of_data.get('pages_on_' + string[string.rfind(' ') + 1:]) * 10 - 10:
                                                           dict_of_data.get('pages_on_' + string[string.rfind(' ') + 1:]) * 10]})
                else:
                    dict_of_data.update({'Table': all_rows})

            dict_of_data.update({
                'name_of_table': string[string.find(':'):],
                'name_of_rows': table.readable_rus(),
            })
            pprint.pprint(dict_of_data)
            return render(request, 'read_table.html', dict_of_data)

        engl_rows = rows = table.readable()[1:]     # получаем поля таблицы , для этого в классе каждой таблицы прописанны поля
        rus_rows = table.readable_rus()[1:]
        dict_of_data.update({'data_for_find': table.readable_rus()})

        ids, rows, code = tuple(x for x in rows if x.find('id_of_') == 0), tuple(x for x in rows if x.find('id_of_') == -1 and x.find('code') == -1), tuple(x for x in rows if x.find('code') > -1)
        engl_ids = tuple(ids)
        # выше на одну строку генерируем два кортежа, один из айдишников, то есть внешних ключей, другой из простых полей

        dict_of_tables = {      # кортеж для получения значений со всех таблиц
            'Country': Country.objects.values_list(),
            'Shape': Shape.objects.values_list(),
            'Medicament': Medicament.objects.values_list(),
            'Pharma_group': Pharma_group.objects.values_list(),
            'Manufacturer': Manufacturer.objects.values_list(),
            'District': District.objects.values_list(),
            'Pharmacy': Pharmacy.objects.values_list(),
            'Lot': Lot.objects.values_list(),
            'Employee': Employee.objects.values_list(),
            'Name_of_medicament': Name_of_medicament.objects.values_list(),
            'Type': Type.objects.values_list(),
        }
        tables = {}     # словарь для вывода на html выдвигающихся полей
        if ids:
            for i in enumerate(tuple(dict_of_tables.get(x[x.find('_of_') + 4:].capitalize()) for x in ids)):    # в tables помещяем внешний ключ + примари ключИ
                if ids[i[0]] in ('id_of_shape', 'id_of_pharma_group', 'id_of_manufacturer', 'id_of_country', 'id_of_district', 'id_of_name_of_medicament', 'id_of_type'):
                    tables.update({ids[i[0]]: tuple(str(j[0]) + ' | ' + j[1] for j in i[1])})  # можно улудшить + названием, но это лень
                elif ids[i[0]] == 'id_of_pharmacy':
                    tables.update({ids[i[0]]: tuple(
                        str(j[0]) + ' | ' + j[2] for j in i[1])})  # можно улудшить + названием, но это лень
                elif ids[i[0]] == 'id_of_lot':
                    tables.update({ids[i[0]]: tuple(
                        str(j[0]) + ' | ' + j[3] for j in i[1])})  # можно улудшить + названием, но это лень
                elif ids[i[0]] == 'id_of_employee':
                    tables.update({ids[i[0]]: tuple(
                        str(j[0]) + ' | ' + j[3] + ' ' + j[2] + ' ' + j[4] for j in i[1])})  # можно улудшить + названием, но это лень
                elif ids[i[0]] == 'id_of_medicament':
                    tables.update({ids[i[0]]: tuple(str(j[0]) + ' | ' + Name_of_medicament.objects.get(id=j[1]).title_of_medicament for j in i[1])})

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

        dict_rows = table.get_attr()    # задаем атрибуты инпутам, что вводить, в каком колве и прочее

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
        elif string.find('Удалить') > -1:
            dict_of_data.update({'template': 'remove_from_table.html'})
            return render(request, 'remove_from_table.html', dict_of_data)
        elif string.find('Изменить') > -1:
            dict_of_data.update({'template': 'update_table.html'})
            return render(request, 'update_table.html', dict_of_data)


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

        # print(dict_of_post)
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
                if dict_of_post.get('defect') == '':
                    del dict_of_post['defect']
                object_of_table.objects.create(**dict_of_post)
                # {'datefact': '2020-02-13', 'count': '2100', 'number_of_lot': '123', 'datestart': '2020-02-10', 'datefinish': '2020-02-22', 'price_manufacturer': '1000', 'price_pharmacy': '2000', 'defect': '1',
                # 'reason': 'Просроченный срок годности', 'id_of_medicament': <Medicament: Medicament object (2)>, 'id_of_employee': <Employee: Employee object (1)>}

                # спам партий
                # for i in range(500):
                #     year, month, day = random.randint(1990, 2019), random.randint(1, 12), random.randint(1, 28)
                #     datefact = datetime.datetime(year=year,
                #                                  month=month,
                #                                  day=day)
                #
                #     datestart = datefact - datetime.datetime(day=datetime.timedelta(days=random.randint(1, 20)))
                #     datefinish = datefact + datetime.datetime(day=datetime.timedelta(days=random.randint(1, 20)))
                #     price_manufacturer, price_pharmacy = random.randint(1, 5999), random.randint(6000, 9999)
                #     defect = random.choice(('0', '1'))
                #     reason = random.choice(('Згнившая упаковка', 'Ужасное состояние', 'Исчерпан срок годности')) if defect == '1' else 'Нет дефекта'
                #     count, number_of_lot = random.randint(1, 9999), random.randint(1, 9999)
                #     dict_of_post.update({'datefact': datefact, 'datestart': datestart, 'datefinish': datefinish,
                #                          'price_manufacturer': price_manufacturer, 'price_pharmacy': price_pharmacy,
                #                          'defect': defect, 'reason': reason, 'count': count, 'number_of_lot': number_of_lot,})

                # ниже спам бд фирмами
                # rb = xlrd.open_workbook('C:\\Users\\kurku\\PycharmProjects\\parse_for_five\\books.xls',
                #                         formatting_info=True)
                # sheet = rb.sheet_by_index(0)
                # for row in range(50, 4337):
                #
                #     html = requests.get('http://www.yopmail.com/ru/email-generator.php',).text
                #     url = html[html.find('onmouseup="this.select();" type="text" value="') + 46:]
                #     dict_of_post['email_of_manufacturer'] = url[:url.find('"')].replace('&#64;', '@')
                #     dict_of_post['year_of_manufacturer'] = str(random.randint(1990, 2020))
                #     dict_of_post['title_of_manufacturer'] = sheet.row_values(row)[0]
                #     if len(dict_of_post.get('title_of_manufacturer')) > 30:
                #         continue
                #     dict_of_post['address_of_manufacturer'] = sheet.row_values(row)[2]
                #     if len(dict_of_post.get('address_of_manufacturer')) > 100:
                #         continue
                #     dict_of_post['id_of_country'] = random.choice(Country.objects.all())

                # ниже, спам бд медикаментами
                # with open('C:\\Users\\kurku\\PycharmProjects\\kursach2kurs2semestr\\medicaments.txt') as f:
                #     for i in f.read().split('\n'):
                #         if 0 < len(i) <= 20:
                #             dict_of_post['title_of_medicament'] = i
                #             try:
                #                 object_of_table.objects.create(**dict_of_post)
                #             except:
                #                 continue

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
