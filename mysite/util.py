import graphics
import datetime
import main

#   ========================================    ЗАДАНИЯ     ================================================


def get_all_medicament_from_all():
    result_of_query = 'SELECT main_lot.id, ' \
                      '     title_of_medicament, ' \
                      '     COUNT(title_of_medicament) as count ' \
                      'FROM main_lot ' \
                      'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ' \
                      'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' \
                      'GROUP BY title_of_medicament ' \
                      'ORDER BY count DESC ' \
                      'LIMIT 5'
    return tuple(row.title_of_medicament for row in main.models.Manufacturer.objects.raw(result_of_query))


def get_all_medicament_from_pharmacy(name_of_pharmacy):
    result_of_query = 'SELECT main_lot.id, title_of_medicament, COUNT(title_of_medicament) as count FROM main_pharmacy ' \
                      'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id AND ' \
                      f'main_pharmacy.id = (SELECT id FROM main_pharmacy WHERE title_of_pharmacy = "{name_of_pharmacy}" ) ' \
                      'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ' \
                      'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ' \
                      'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' \
                      'GROUP BY title_of_medicament ' \
                      'ORDER BY count DESC ' \
                      'LIMIT 5'
    return tuple(row.title_of_medicament for row in main.models.Manufacturer.objects.raw(result_of_query))


def get_all_medicament_from_district(name_of_district):

    result_of_query = 'SELECT main_lot.id, title_of_medicament, COUNT(title_of_medicament) as count FROM main_district ' \
                      'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id AND ' \
                      f'main_district.id = (SELECT id FROM main_district WHERE title_of_district = "{name_of_district}") ' \
                      'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
                      'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ' \
                      'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ' \
                      'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' \
                      'GROUP BY title_of_medicament ' \
                      'ORDER BY count DESC ' \
                      'LIMIT 5'
    return tuple(row.title_of_medicament for row in main.models.Manufacturer.objects.raw(result_of_query))


def get_all_pharmacy_from_all():
    result_of_query = 'SELECT main_pharmacy.id, title_of_type, COUNT(title_of_type) as count FROM main_district ' \
                      'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
                      'INNER JOIN main_type ON main_type.id = main_pharmacy.id_of_type_id ' \
                      'GROUP BY title_of_type ' \
                      'ORDER BY count DESC'
    return tuple(row.title_of_type + ': ' + str(row.count) for row in main.models.Manufacturer.objects.raw(result_of_query))


def get_all_pharmacy_from_district(name_of_district):
    result_of_query = 'SELECT main_pharmacy.id, title_of_type, COUNT(title_of_type) as count FROM main_district ' \
                      'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id AND ' \
                      f'main_district.id = (SELECT id FROM main_district WHERE title_of_district = "{name_of_district}") ' \
                      'INNER JOIN main_type ON main_type.id = main_pharmacy.id_of_type_id ' \
                      'GROUP BY title_of_type ' \
                      'ORDER BY count DESC'
    return tuple(row.title_of_type + ': ' + str(row.count) for row in main.models.Manufacturer.objects.raw(result_of_query))


def get_all_comebacks_from_all():
    result_of_query = 'SELECT main_medicament.id, SUM(main_lot.price_manufacturer) as sum, COUNT(main_lot.defect) as count FROM main_manufacturer ' \
                      'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id ' \
                      'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id WHERE defect="1" '
    return tuple('Сумма: ' + str(row.sum) + ', Количество возвратов: ' + str(row.count) for row in main.models.Manufacturer.objects.raw(result_of_query))


def get_all_comebacks_from_manufacturer(name_of_manufacturer):
    result_of_query = 'SELECT main_medicament.id, SUM(main_lot.price_manufacturer) as sum, COUNT(main_lot.defect) as count FROM main_manufacturer ' \
                      'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id AND ' \
                      f'main_manufacturer.id = (SELECT id FROM main_manufacturer WHERE title_of_manufacturer = "{name_of_manufacturer}") ' \
                      'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id WHERE defect="1" '
    return tuple('Сумма: ' + str(row.sum) + ', Количество возвратов: ' + str(row.count) for row in main.models.Manufacturer.objects.raw(result_of_query))


#   ========================================    ЗАПРОСЫ     ================================================


def get_amount_pharmacy_type_in_district(main_district_id):     # получение количества типов аптек по району с ID 1 (для одномерного графика)
    """
        Первый запрос, на внутренний джоин
    :param main_district_id:
    :return:
    """
    query = 'SELECT main_pharmacy.id, main_type.title_of_type as Название_типа, ' \
            '       COUNT(main_pharmacy.id_of_type_id) as Количество_аптек_данного_типа ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ' \
            f'   AND main_district.id = "{main_district_id}" ' \
            'INNER JOIN main_type ON main_type.id = main_pharmacy.id_of_type_id ' \
            'GROUP BY main_pharmacy.id_of_type_id'
    result_of_query = tuple({'Название_типа': row.Название_типа, 'Количество_аптек_данного_типа':row.Количество_аптек_данного_типа} for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT main_pharmacy.id_of_type_id as id_типа, COUNT(main_pharmacy.id_of_type_id) as Количество_аптек_данного_типа ||' \
           'FROM main_district ||' \
           'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ||' \
           f'   AND main_district.id = "{main_district_id}" ||' \
           'GROUP BY main_pharmacy.id_of_type_id ||'.split('||'), \
           graphics.first_graphic(labels=tuple(row.get("Название_типа") for row in result_of_query),
                                  values=tuple(row.get("Количество_аптек_данного_типа") for row in result_of_query))


def get_amount_of_medicaments(main_pharmacy_id):    # получение медикаментов из аптеки
    """
        Второй запрос, на внутренний джоин
    :param main_pharmacy_id:
    :return:
    """
    query = 'SELECT main_name_of_medicament.id, title_of_medicament AS Название_медикамента, ' \
            '       COUNT(title_of_medicament) AS Количество_доставок ' \
            'FROM ' \
            '   (SELECT main_lot.id_of_medicament_id ' \
            '   FROM main_lot ' \
            '   INNER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ' \
            '   INNER JOIN main_pharmacy ON main_pharmacy.id = main_employee.id_of_pharmacy_id ' \
            f'       AND main_pharmacy.id = "{main_pharmacy_id}") AS medicament_in_pharm ' \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = medicament_in_pharm.id_of_medicament_id ' \
            'GROUP BY title_of_medicament'
    result_of_query = tuple({'Название_медикамента': row.Название_медикамента, 'Количество_доставок': row.Количество_доставок} for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT title_of_medicament AS Название_медикамента, COUNT(title_of_medicament) AS Количество_доставок FROM ||' \
           '   (SELECT main_lot.id_of_medicament_id ||' \
           '   FROM main_lot ||' \
           '   INNER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ||' \
           '   INNER JOIN main_pharmacy ON main_pharmacy.id = main_employee.id_of_pharmacy_id ||' \
           f'       AND main_pharmacy.id = "{main_pharmacy_id}") AS medicament_in_pharm ||' \
           'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = medicament_in_pharm.id_of_medicament_id ||' \
           'GROUP BY title_of_medicament'.split('||'), \
           graphics.second_graphic(x=tuple(row.get('Название_медикамента') for row in result_of_query),
                                   y=tuple(row.get('Количество_доставок') for row in result_of_query),
                                   name_x='Название медикамента',
                                   name_y='Количество доставок')


def get_lot_of_after(datefact):    # получение партий после определенного числа
    """
        Третий запрос на внутренний джоин но по датам
    :param datefact:
    :return:
    """
    main_pharmacy_id = datefact[0][:datefact[0].find(' ')]
    query = 'SELECT lot.id, lot.datefact AS Дата_доставки, ' \
            '       lot.count AS Количество, ' \
            '       lot.number_of_lot AS Номер_партии, ' \
            '       lot.datestart AS Дата_изготовления, ' \
            '       lot.datefinish AS Срок_годности, ' \
            '       lot.price_manufacturer AS Цена_фирмы, ' \
            '       lot.price_pharmacy AS Цена_аптеки, ' \
            '       lot.defect AS Дефект, ' \
            '       CONCAT(main_employee.second_name, " ", LEFT(main_employee.first_name, 1), ". ", LEFT(main_employee.third_name, 1), ".") AS Принявший_сотрудник '   \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}" '  \
            'INNER JOIN main_lot as lot ON lot.id_of_employee_id = main_employee.id '  \
            f'   AND lot.datefact > "{datefact[1]}" '
    result_of_query = tuple({'Дата_доставки': row.Дата_доставки,
                             'Количество': row.Количество,
                             'Номер_партии': row.Номер_партии,
                             'Дата_изготовления': row.Дата_изготовления,
                             'Срок_годности': row.Срок_годности,
                             'Цена_фирмы': row.Цена_фирмы,
                             'Цена_аптеки': row.Цена_аптеки,
                             'Принявший_сотрудник': row.Принявший_сотрудник,
                             } for row in main.models.Manufacturer.objects.raw(query))
    for row in result_of_query:
        row['Дата_доставки'] = row.get('Дата_доставки').strftime('%Y-%m-%d')
        row['Дата_изготовления'] = row.get('Дата_изготовления').strftime('%Y-%m-%d')
        row['Срок_годности'] = row.get('Срок_годности').strftime('%Y-%m-%d')
    return result_of_query, \
           'SELECT lot.id, lot.datefact AS Дата_доставки, lot.count AS Количество, lot.number_of_lot AS Номер_партии, ||' \
            '    lot.datestart AS Дата_изготовления, lot.datefinish AS Срок_годности, lot.price_manufacturer AS Цена_фирмы, ||' \
            '    lot.price_pharmacy AS Цена_аптеки, lot.defect AS Дефект, ||' \
            '    CONCAT(main_employee.second_name, " ", LEFT(main_employee.first_name, 1), ". ", LEFT(main_employee.third_name, 1), ".") AS Принявший_сотрудник ||'   \
            'FROM main_pharmacy ||' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}" ||'  \
            'INNER JOIN main_lot as lot ON lot.id_of_employee_id = main_employee.id ||'  \
            f'   AND main_lot.datefact > "{datefact[1]}" '.split('||')


def get_lot_of_between(datefact):    # получение партий между отпределенными датами
    """
        Четвертый запрос на внутренний джоин но по датам
    :param datefact:
    :return:
    """
    main_pharmacy_id = datefact[0][:datefact[0].find(' ')]
    query = 'SELECT lot.id, lot.datefact AS Дата_доставки, ' \
            '       lot.count AS Количество, ' \
            '       lot.number_of_lot AS Номер_партии, ' \
            '       lot.datestart AS Дата_изготовления, ' \
            '       lot.datefinish AS Срок_годности, ' \
            '       lot.price_manufacturer AS Цена_фирмы, ' \
            '       lot.price_pharmacy AS Цена_аптеки, ' \
            '       lot.defect AS Дефект, ' \
            '       CONCAT(main_employee.second_name, " ", LEFT(main_employee.first_name, 1), ". ", LEFT(main_employee.third_name, 1), ".") AS Принявший_сотрудник '   \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}" '  \
            'INNER JOIN main_lot as lot ON lot.id_of_employee_id = main_employee.id '  \
            f'   AND lot.datefact BETWEEN "{datefact[1]}" AND "{datefact[2]}" '
    result_of_query = tuple({'Дата_доставки': row.Дата_доставки,
                             'Количество': row.Количество,
                             'Номер_партии': row.Номер_партии,
                             'Дата_изготовления': row.Дата_изготовления,
                             'Срок_годности': row.Срок_годности,
                             'Цена_фирмы': row.Цена_фирмы,
                             'Цена_аптеки': row.Цена_аптеки,
                             'Дефект': row.Дефект,
                             'Принявший_сотрудник': row.Принявший_сотрудник,
                             } for row in main.models.Manufacturer.objects.raw(query))
    for row in result_of_query:
        row['Дата_доставки'] = row.get('Дата_доставки').strftime('%Y-%m-%d')
        row['Дата_изготовления'] = row.get('Дата_изготовления').strftime('%Y-%m-%d')
        row['Срок_годности'] = row.get('Срок_годности').strftime('%Y-%m-%d')
    return result_of_query, \
           'SELECT lot.id, lot.datefact AS Дата_доставки, lot.count AS Количество, lot.number_of_lot AS Номер_партии, ||' \
            '    lot.datestart AS Дата_изготовления, lot.datefinish AS Срок_годности, lot.price_manufacturer AS Цена_фирмы, ||' \
            '    lot.price_pharmacy AS Цена_аптеки, lot.defect AS Дефект, ||' \
            '    CONCAT(main_employee.second_name, " ", LEFT(main_employee.first_name, 1), ". ", LEFT(main_employee.third_name, 1), ".") AS Принявший_сотрудник ||'   \
            'FROM main_pharmacy ||' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}" ||'  \
            'INNER JOIN main_lot as lot ON lot.id_of_employee_id = main_employee.id ||'  \
            f'   AND lot.datefact BETWEEN "{datefact[1]}" AND "{datefact[2]}" '.split('||')


def get_all_about_medicaments():    # получение всех существующих лекарств
    """
        Пятый запрос на получение всех существующих лекарств.
        (join без условия, первый запрос)
    :return:
    """
    query = 'SELECT main_name_of_medicament.id, ' \
            '       main_name_of_medicament.title_of_medicament AS Название_лекарства, ' \
            '       main_pharma_group.title_of_pharma_group AS Фармакалогичесикая_группа, ' \
            '       main_manufacturer.title_of_manufacturer AS Издатель, ' \
            '       main_shape.title_of_shape AS Форма_выпуска, ' \
            '       main_medicament.comments AS Инструкция ' \
            'FROM main_medicament ' \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' \
            'INNER JOIN main_pharma_group ON main_pharma_group.id = main_medicament.id_of_pharma_group_id ' \
            'INNER JOIN main_manufacturer ON main_manufacturer.id = main_medicament.id_of_manufacturer_id ' \
            'INNER JOIN main_shape ON main_shape.id = main_medicament.id_of_shape_id '
    result_of_query = tuple({'Название_лекарства': row.Название_лекарства,
                             'Фармакалогичесикая_группа': row.Фармакалогичесикая_группа,
                             'Издатель': row.Издатель,
                             'Форма_выпуска': row.Форма_выпуска,
                             'Инструкция': row.Инструкция,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT ' \
            '       main_name_of_medicament.title_of_medicament AS Название_лекарства, ||' \
            '       main_pharma_group.title_of_pharma_group AS Фармакалогичесикая_группа, ||' \
            '       main_manufacturer.title_of_manufacturer AS Издатель, ||' \
            '       main_shape.title_of_shape AS Форма_выпуска, ||' \
            '       main_medicament.comments AS Инструкция ||' \
            'FROM main_medicament ||' \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ||' \
            'INNER JOIN main_pharma_group ON main_pharma_group.id = main_medicament.id_of_pharma_group_id ||' \
            'INNER JOIN main_manufacturer ON main_manufacturer.id = main_medicament.id_of_manufacturer_id ||' \
            'INNER JOIN main_shape ON main_shape.id = main_medicament.id_of_shape_id '.split('||')


def get_all_employeers():   # получение всех работников определенной аптеки
    """
        Шестой запрос на получение всех существующих работников.
        (join без условия, второй запрос)
    :return:
    """
    query = 'SELECT main_pharmacy.id, ' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
            '       main_employee.second_name AS Фамилия, ' \
            '       main_employee.first_name AS Имя, ' \
            '       main_employee.third_name AS Отчество '  \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id '
    result_of_query = tuple({'Название_аптеки': row.Название_аптеки,
                             'Фамилия': row.Фамилия,
                             'Имя': row.Имя,
                             'Отчество': row.Отчество,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
           '       main_employee.second_name AS Фамилия, ||' \
           '       main_employee.first_name AS Имя, ||' \
           '       main_employee.third_name AS Отчество ||'  \
           'FROM main_pharmacy ||' \
           'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||'.split('||')


def get_employee_from_district():
    """
        Седьмой запрос на получение всех существующих работников по всем районам.
        (join без условия, третий запрос)
    :return:
    """
    query = 'SELECT main_pharmacy.id, ' \
            '       main_district.title_of_district AS Название_района, ' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
            '       main_employee.second_name AS Фамилия, ' \
            '       main_employee.first_name AS Имя, ' \
            '       main_employee.third_name AS Отчество, ' \
            '       main_lot.id AS id_партии,' \
            '       main_lot.datefact AS Дата_приема ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id '
    result_of_query = tuple({'Название_района': row.Название_района,
                             'Название_аптеки': row.Название_аптеки,
                             'Фамилия': row.Фамилия,
                             'Имя': row.Имя,
                             'Отчество': row.Отчество,
                             'id_партии': row.id_партии,
                             'Дата_приема': row.Дата_приема,
                             } for row in main.models.Manufacturer.objects.raw(query))
    for row in result_of_query:
        row['Дата_приема'] = row.get('Дата_приема').strftime('%Y-%m-%d')
    return result_of_query, \
           'SELECT ||' \
            '       main_district.title_of_district AS Название_района, ||' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
            '       main_employee.second_name AS Фамилия, ||' \
            '       main_employee.first_name AS Имя, ||' \
            '       main_employee.third_name AS Отчество ||' \
            '       main_lot.number_of_lot AS Номер_партии, ||' \
            '       main_lot.datefact AS Дата_приема ||' \
            'FROM main_district ||' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ||' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
            'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id '.split('||')


def get_all_unknown_medicaments():
    """
        Восьмой запрос на левое внешнее соединение.
    :return:
    """
    query = 'SELECT main_manufacturer.id, ' \
            '       main_name_of_medicament.title_of_medicament AS Название_лекарства, ' \
            '       main_pharma_group.title_of_pharma_group AS Фармакалогичесикая_группа, ' \
            '       main_manufacturer.title_of_manufacturer AS Издатель, ' \
            '       main_shape.title_of_shape AS Форма_выпуска, ' \
            '       main_medicament.comments AS Инструкция ' \
            'FROM main_medicament ' \
            'LEFT OUTER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ' \
            'LEFT OUTER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' \
            'LEFT OUTER JOIN main_pharma_group ON main_pharma_group.id = main_medicament.id_of_pharma_group_id ' \
            'LEFT OUTER JOIN main_manufacturer ON main_manufacturer.id = main_medicament.id_of_manufacturer_id ' \
            'LEFT OUTER JOIN main_shape ON main_shape.id = main_medicament.id_of_shape_id ' \
            f'WHERE main_lot.id_of_medicament_id IS NULL'
    result_of_query = tuple({'Название_лекарства': row.Название_лекарства,
                             'Фармакалогичесикая_группа': row.Фармакалогичесикая_группа,
                             'Издатель': row.Издатель,
                             'Форма_выпуска': row.Форма_выпуска,
                             'Инструкция': row.Инструкция,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT ||' \
           '       main_name_of_medicament.title_of_medicament AS Название_лекарства, ||' \
           '       main_pharma_group.title_of_pharma_group AS Фармакалогичесикая_группа, ||' \
           '       main_manufacturer.title_of_manufacturer AS Издатель, ||' \
           '       main_shape.title_of_shape AS Форма_выпуска, ||' \
           '       main_medicament.comments AS Инструкция ||' \
           'FROM main_medicament ||' \
           'LEFT OUTER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ||' \
           'LEFT OUTER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ||' \
           'LEFT OUTER JOIN main_pharma_group ON main_pharma_group.id = main_medicament.id_of_pharma_group_id ||' \
           'LEFT OUTER JOIN main_manufacturer ON main_manufacturer.id = main_medicament.id_of_manufacturer_id ||' \
           'LEFT OUTER JOIN main_shape ON main_shape.id = main_medicament.id_of_shape_id ||' \
           f'WHERE main_lot.id_of_medicament_id IS NULL'.split('||')


def get_all_employee_who_not_get_lot():
    """
        Девятый запрос на правое внешнее соединение.
    :return:
    """
    query = 'SELECT main_pharmacy.id, ' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
            '       main_employee.second_name AS Фамилия, ' \
            '       main_employee.first_name AS Имя, ' \
            '       main_employee.third_name AS Отчество ' \
            'FROM main_lot ' \
            'RIGHT OUTER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ' \
            'LEFT JOIN main_pharmacy ON main_pharmacy.id = main_employee.id_of_pharmacy_id ' \
            'WHERE main_lot.id IS NULL'
    result_of_query = tuple({'Название_аптеки': row.Название_аптеки,
                             'Фамилия': row.Фамилия,
                             'Имя': row.Имя,
                             'Отчество': row.Отчество,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT ||' \
           '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
           '       main_employee.second_name AS Фамилия, ||' \
           '       main_employee.first_name AS Имя, ||' \
           '       main_employee.third_name AS Отчество ||' \
           'FROM main_lot ||' \
           'RIGHT OUTER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ||' \
           'LEFT JOIN main_pharmacy ON main_pharmacy.id = main_employee.id_of_pharmacy_id ||' \
           'WHERE main_lot.id IS NULL'.split('||')


def get_defect_from_manufact(main_manufacturer_id):     # смотрим все дефекты для определенной фирмы
    """
        Десятый запрос на inner с leftom.
    :param main_manufacturer_id:
    :return:
    """
    query = 'SELECT main_reason.id, ' \
            '       name.title_of_medicament AS Название_лекарства, ' \
            '       main_reason.title_of_reason AS Причина_возврата, ' \
            '       main_lot.datestart AS Дата_создания '  \
            'FROM main_manufacturer '  \
            'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id ' \
            f'   AND main_manufacturer.id = "{main_manufacturer_id}" '  \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ' \
            '   AND main_lot.defect = "1" ' \
            'LEFT JOIN main_name_of_medicament as name ON name.id = main_medicament.id_of_name_of_medicament_id ' \
            'INNER JOIN main_reason ON main_reason.id = main_lot.id_of_reason_id'
    result_of_query = tuple({'Название_лекарства': row.Название_лекарства,
                             'Причина_возврата': row.Причина_возврата,
                             'Дата_создания': row.Дата_создания,
                             } for row in main.models.Manufacturer.objects.raw(query))
    for row in result_of_query:
        row['Дата_создания'] = row.get('Дата_создания').strftime('%Y-%m-%d')
    return result_of_query, \
           'SELECT name.title_of_medicament AS Название_лекарства, main_lot.reason AS Причина_возврата, ||' \
            '   main_lot.datestart AS Дата_создания ||'  \
            'FROM main_manufacturer ||'  \
            'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id ||' \
            f'   AND main_manufacturer.id = "{main_manufacturer_id}" ||'  \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ||' \
            '   AND main_lot.defect = "1" ||' \
            'LEFT JOIN main_name_of_medicament as name ON name.id = main_medicament.id_of_name_of_medicament_id ||' \
            'INNER JOIN main_reason ON main_reason.id = main_lot.id_of_reason'.split('||'), \
            graphics.third_graphic(x=tuple(row.get('Название_лекарства') for row in result_of_query),
                                   y=tuple(row.get('Причина_возврата') for row in result_of_query),
                                   z=tuple(row.get('Дата_создания') for row in result_of_query), )


##################################################################################################################

# ================================================ ЗАДАНИЯ ДЛЯ СЕДЬМОЙ ЛАБЫ ======================================

##################################################################################################################


def get_all_employeers_in_db():
    """
        Одинадцатый запрос, итоговый запрос без условия.
    :return:
    """
    query = 'SELECT id,' \
            '       first_name AS Имя,' \
            '       second_name AS Фамилия, ' \
            '       third_name AS Отчество ' \
            'FROM main_employee'
    result_of_query = tuple({'Имя': row.Имя,
                             'Фамилия': row.Фамилия,
                             'Отчество': row.Отчество,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT id, ||' \
           '       first_name AS Имя, ||' \
           '       second_name AS Фамилия, ||' \
           '       third_name AS Отчество ||' \
           'FROM main_employee'.split('||')


def get_all_medicament_from_manufact(id_of_manufacturer_id):
    """
        Двенадцатый запрос с условием на данные.
    :return:
    """
    query = 'SELECT main_lot.id, ' \
            '       main_name_of_medicament.title_of_medicament AS Название_лекарства,' \
            '       main_lot.datefact AS Дата_доставки, ' \
            '       main_lot.number_of_lot AS Номер_партии, ' \
            '       main_lot.count AS Количество, ' \
            '       main_lot.price_manufacturer AS Цена_фирмы, ' \
            '       main_lot.defect AS Дефект ' \
            'FROM main_medicament ' \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ' \
            f'   AND main_medicament.id_of_manufacturer_id = "{id_of_manufacturer_id}" ' \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id '
    result_of_query = tuple({'Название_лекарства': row.Название_лекарства,
                             'Дата_доставки': row.Дата_доставки,
                             'Номер_партии': row.Номер_партии,
                             'Количество': row.Количество,
                             'Цена_фирмы': row.Цена_фирмы,
                             'Дефект': row.Дефект,
                             } for row in main.models.Manufacturer.objects.raw(query))
    for row in result_of_query:
        row['Дата_доставки'] = row.get('Дата_доставки').strftime('%Y-%m-%d')
    return result_of_query, \
           'SELECT main_name_of_medicament.title_of_medicament AS Название_лекарства, ||' \
            '       main_lot.datefact AS Дата_доставки, ||' \
            '       main_lot.number_of_lot AS Номер_партии, ||' \
            '       main_lot.count AS Количество, ||' \
            '       main_lot.price_manufacturer AS Цена_фирмы, ||' \
            '       main_lot.defect AS Дефект ||' \
            'FROM main_medicament ||' \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ||' \
            f'   AND main_medicament.id_of_manufacturer_id = "{id_of_manufacturer_id}"||' \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id '.split('||')


# def get_medicament_with_define_shape(tenth_query):
#     """
#         Двенадцатый запрос с условием на данные.
#     :param tenth_query:
#     :return:
#     """
#     main_name_of_medicament_id = tenth_query[0][:tenth_query[0].find(' ')]
#     main_shape_id = tenth_query[1][:tenth_query[1].find(' ')]
#     main_district_id = tenth_query[2][:tenth_query[2].find(' ')]
#     query = 'SELECT ' \
#             '       main_lot.price_pharmacy AS Цена, ' \
#             '       main_lot.datefact AS Срок_годности, ' \
#             '       main_lot.count AS Количество, ' \
#             '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
#             '       main_pharmacy.phone_of_pharmacy AS Телефон, ' \
#             '       main_pharmacy.address_of_pharmacy AS Адрес ' \
#             'FROM main_pharmacy ' \
#             'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
#             f'   AND main_pharmacy.id_of_district_id = {main_district_id} ' \
#             'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ' \
#             '   AND main_lot.defect = "0" ' \
#             f'INNER JOIN main_medicament ON main_medicament.id_of_shape_id = {main_shape_id} ' \
#             f'  AND main_medicament.id_of_name_of_medicament_id = {main_name_of_medicament_id}'
#     result_of_query = execute(query)
#     return result_of_query, \
#            'SELECT ' \
#             '       main_lot.price_pharmacy AS Цена, ||' \
#             '       main_lot.datefact AS Срок_годности, ||' \
#             '       main_lot.count AS Количество, ||' \
#             '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
#             '       main_pharmacy.phone_of_pharmacy AS Телефон, ||' \
#             '       main_pharmacy.address_of_pharmacy AS Адрес, ||' \
#             'FROM main_pharmacy ||' \
#             'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
#             f'   AND main_pharmacy.id_of_district_id = {main_district_id} ||' \
#             'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ||' \
#             '   AND main_lot.defect = "0" ||' \
#             f'INNER JOIN main_medicament ON main_medicament.id_of_shape_id = {main_shape_id} ||' \
#             f'  AND main_medicament.id_of_name_of_medicament_id = {main_name_of_medicament_id}'.split('||')


def get_medicament_with_right_join(worker):    # получаем все лекарства принимаемые каким-то одним работником
    """
        Тринадцатый запрос с условием на группы.
    :param worker:
    :return:
    """
    query = 'SELECT main_lot.id, ' \
            '       main_lot.number_of_lot AS Номер_партии, ' \
            '       main_lot.datefact AS Дата_приема, '  \
            '       main_lot.datestart AS Дата_создания, '  \
            '       main_lot.datefinish AS Срок_годности, '  \
            '       main_lot.price_manufacturer AS Цена_фирмы, '  \
            '       main_lot.price_pharmacy AS Цена_аптеки, '  \
            '       main_lot.defect AS Наличие_дефекта, '  \
            '       main_lot.reason AS Причина_дефекта '  \
            'FROM main_lot ' \
            'INNER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ' \
            f'   AND main_employee.id = "{worker}" ' \
            'GROUP BY main_lot.id '
    result_of_query = tuple({'Номер_партии': row.Номер_партии,
                             'Дата_приема': row.Дата_приема,
                             'Дата_создания': row.Дата_создания,
                             'Срок_годности': row.Срок_годности,
                             'Цена_фирмы': row.Цена_фирмы,
                             'Цена_аптеки': row.Цена_аптеки,
                             'Наличие_дефекта': row.Наличие_дефекта,
                             'Причина_дефекта': row.Причина_дефекта,
                             } for row in main.models.Manufacturer.objects.raw(query))
    for row in result_of_query:
        row['Дата_приема'] = row.get('Дата_приема').strftime('%Y-%m-%d')
        row['Дата_создания'] = row.get('Дата_создания').strftime('%Y-%m-%d')
        row['Срок_годности'] = row.get('Срок_годности').strftime('%Y-%m-%d')
    return result_of_query, \
           'SELECT main_lot.id, ||' \
            '       main_lot.number_of_lot AS Номер_партии, ||' \
            '       main_lot.datefact AS Дата_приема, ||'  \
            '       main_lot.datestart AS Дата_создания, ||'  \
            '       main_lot.datefinish AS Срок_годности, ||'  \
            '       main_lot.price_manufacturer AS Цена_фирмы, ||'  \
            '       main_lot.price_pharmacy AS Цена_аптеки, ||'  \
            '       main_lot.defect AS Наличие_дефекта, ||'  \
            '       main_lot.reason AS Причина_дефекта ||'  \
            'FROM main_lot ||' \
            'INNER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ||' \
            f'   AND main_employee.id = "{worker}" ||' \
            'GROUP BY main_lot.id '.split('||')


def get_amount_of_employeers_in_pharmacy(main_district_id):
    """
        Запрос на группы, но не использующийся.
    :param main_district_id:
    :return:
    """
    query = 'SELECT main_pharmacy.id, ' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
            '       COUNT(main_employee.id) AS Количество_работников ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
            f'   AND main_district.id = {main_district_id} ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            'GROUP BY main_pharmacy.title_of_pharmacy '
    result_of_query = tuple({'Название_аптеки': row.Название_аптеки,
                             'Количество_работников': row.Количество_работников,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
            '       COUNT(main_employee.id) AS Количество_работников ||' \
            'FROM main_district ||' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ||' \
            f'   AND main_district.id = {main_district_id} ||' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
            'GROUP BY main_pharmacy.title_of_pharmacy '.split('||')


def get_cheap_medicaments(get_all_data):
    """
        Четырнадцатый запрос на группы + данные + с подзапросом.
    :param get_all_data:
    :return:
    """
    main_district_id = get_all_data[1][:get_all_data[1].find(' ')]
    main_medicament_id = get_all_data[0][:get_all_data[0].find(' ')]
    # подказпрос который возвращает все найденные лекарства в данном регионе
    sub_query = 'SELECT main_pharmacy.id, ' \
                '       main_lot.count AS Количество_препарата, ' \
                '       main_lot.price_pharmacy AS Цена_препарата, ' \
                '       main_pharmacy.title_of_pharmacy AS Название_аптеки,' \
                '       main_lot.price_pharmacy / main_lot.count AS КПД ' \
                'FROM main_district ' \
                'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
                f'   AND main_district.id = "{main_district_id}" ' \
                'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
                'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ' \
                'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ' \
                f'   AND main_medicament.id = "{main_medicament_id}" ' \
                'ORDER BY КПД DESC ' \
                f'LIMIT {2**64-1}'     #  кастыль MARIADB
    query = 'SELECT list_medicaments.id, ' \
            '       Количество_препарата,' \
            '       Цена_препарата, ' \
            '       Название_аптеки ' \
            f'FROM ({sub_query}) AS list_medicaments ' \
            'GROUP BY list_medicaments.Название_аптеки '
    result_of_query = tuple({'Количество_препарата': row.Количество_препарата,
                             'Цена_препарата': row.Цена_препарата,
                             'Название_аптеки': row.Название_аптеки,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT Количество_препарата, ||' \
           '       Цена_препарата, ||' \
           '       Название_аптеки ||' \
           f'FROM (||' \
           '            SELECT ||' \
           '                   main_lot.count AS Количество_препарата, ||' \
           '                   main_lot.price_pharmacy AS Цена_препарата, ||' \
           '                   main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
           '                   main_lot.price_pharmacy / main_lot.count AS КПД ||' \
           '            FROM main_district ||' \
           '            INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ||' \
           f'              AND main_district.id = "{main_district_id}" ||' \
           '            INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
           '            INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ||' \
           '            INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ||' \
           f'              AND main_medicament.id = "{main_medicament_id}" ||' \
           '            ORDER BY КПД DESC ||' \
           f'           LIMIT {2 ** 64 - 1} ||' \
           ') AS list_medicaments ||' \
           'GROUP BY list_medicaments.Название_аптеки'.split('||')


def get_cheap_all_medicaments(main_district_id):
    """
        Пятнадцатый запрос итоговый запрос по приницпу запроса.
    :param get_all_data:
    :return:
    """
    # подказпрос который возвращает все найденные лекарства в данном регионе
    sub_query = 'SELECT main_pharmacy.id, ' \
                '       main_lot.count AS Количество_препарата, ' \
                '       main_name_of_medicament.title_of_medicament AS Название_лекарства, ' \
                '       main_lot.price_pharmacy AS Цена_препарата, ' \
                '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
                '       main_lot.price_pharmacy / main_lot.count AS КПД ' \
                'FROM main_district ' \
                'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
                f'   AND main_district.id = "{main_district_id}" ' \
                'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
                'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ' \
                'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ' \
                'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' \
                'ORDER BY КПД DESC ' \
                f'LIMIT {2**64-1}'     #  кастыль MARIADB
    query = 'SELECT list_medicaments.id, ' \
            '       Название_лекарства, ' \
            '       Количество_препарата,' \
            '       Цена_препарата, ' \
            '       Название_аптеки ' \
            f'FROM ({sub_query}) AS list_medicaments ' \
            'GROUP BY list_medicaments.Название_лекарства '
    result_of_query = tuple({'Название_лекарства': row.Название_лекарства,
                             'Количество_препарата': row.Количество_препарата,
                             'Цена_препарата': row.Цена_препарата,
                             'Название_аптеки': row.Название_аптеки,
                             } for row in main.models.Manufacturer.objects.raw(query))
    return result_of_query, \
           'SELECT Название_лекарства, ||' \
           '       Количество_препарата, ||' \
           '       Цена_препарата, ||' \
           '       Название_аптеки ||' \
           f'FROM (||' \
           '        SELECT ||' \
           '            main_lot.count AS Количество_препарата, ||' \
           '            main_name_of_medicament.title_of_medicament AS Название_лекарства, ||' \
           '            main_lot.price_pharmacy AS Цена_препарата, ||' \
           '            main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
           '            main_lot.price_pharmacy / main_lot.count AS КПД ||' \
           '        FROM main_district ||' \
           '        INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ||' \
           f'           AND main_district.id = "{main_district_id}" ||' \
           '        INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
           '        INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ||' \
           '        INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ||' \
           '        INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ||' \
           '        ORDER BY КПД DESC ||' \
           f'       LIMIT {2**64-1}||' \
           ') AS list_medicaments ||' \
           'GROUP BY list_medicaments.Название_лекарства'.split('||')


def sum_all_methods_for_querys(get_all_data):

    return {
            '<h3>1.Вывод всех типов аптек (и количество аптек) по заданному району.<br>(первый внутренний запрос по внешнему ключу)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('first_querys')[0]}</div>":
                get_amount_pharmacy_type_in_district(get_all_data.get('first_querys')[0][:get_all_data.get('first_querys')[0].find('|') -1]),

            '<h3>2.Вывод всех медикаментов из заданной аптеки.<br>(второй внутренний запрос по внешнему ключу)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('second_querys')[0]}</div>":
                get_amount_of_medicaments(get_all_data.get('second_querys')[0][:get_all_data.get('second_querys')[0].find('|') -1]),

            f'<h3>3.Получение всех партий после {get_all_data.get("third_querys")[1]}<br>(первый внутренний запрос по дате)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{', '.join(get_all_data.get('third_querys'))} </div>":
                get_lot_of_after(get_all_data.get('third_querys')),

            f'<h3>4.Получение всех партий между {get_all_data.get("fourth_querys")[1]} и {get_all_data.get("fourth_querys")[2]}<br>(второй внутренний запрос по дате)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{', '.join(get_all_data.get('fourth_querys'))} </div>":
                get_lot_of_between(get_all_data.get('fourth_querys')),

            '<h3>5.Получение всех существующих лекарств<br>(первый внутренне симметричный запрос)</h3>':
                get_all_about_medicaments(),

            '<h3>6.Получение всех работников c аптеками<br>(второй внутренне симметричный запрос)</h3>':
                get_all_employeers(),

            '<h3>7.Получение всех работников получивших партии, и вывод их партий<br>(третий внутренне симметричный запрос)</h3>':
                get_employee_from_district(),
                # get_medicament_with_right_join(get_all_data.get('eigth_querys')[0][:get_all_data.get('eigth_querys')[0].find(' ')]),

            '<h3>8.Получение всех непоставляемых лекарств<br>(левое внешнее соединение)</h3>':
                get_all_unknown_medicaments(),

            '<h3>9.Получение всех сотрудников которые не получали не одной партии<br>(правое внешнее соединение)</h3>':
                get_all_employee_who_not_get_lot(),

            '<h3>10.Получение всех возвратов и их причин по определенной фирме<br>(запрос по принципу левого соединения)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('fifth_querys')[0]} </div>":
                get_defect_from_manufact(
                    get_all_data.get('fifth_querys')[0][:get_all_data.get('fifth_querys')[0].find(' ')]),

            '<h3>11.Получение всех сотрудников всех аптек<br>(итоговый запрос без условия)</h3>':
                get_all_employeers_in_db(),

            '<h3>12.Получение всех доставок определенной фирмы.<br>(итоговый запрос с условием на данные)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('twelfth_querys')[0]} </div>":
                get_all_medicament_from_manufact(get_all_data.get('twelfth_querys')[0][:get_all_data.get('twelfth_querys')[0].find(' ')]),

            '<h3>13.Получение количества всех сотрудников всех аптек по району<br>(итоговый запрос с условием на группы)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('thirdth_querys')[0]} </div>":
                get_amount_of_employeers_in_pharmacy(get_all_data.get('thirdth_querys')[0][:get_all_data.get('thirdth_querys')[0].find(' ')]),

            '<h3>14.Получение всех дешевых препаратов по району<br>(запрос на запросе по принципу итогового запроса)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('fifteenth_querys')[0]} </div>":
                get_cheap_all_medicaments(
                    get_all_data.get('fifteenth_querys')[0][:get_all_data.get('fifth_querys')[0].find(' ')]),

            '<h3>15.Получение всех дешевых препаратов по району<br>(итоговый запрос с условием на группы и данные + запрос с подзапросом)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{', '.join(get_all_data.get('twelveth_querys'))} </div>":
                get_cheap_medicaments(get_all_data.get('twelveth_querys')),

            }


if __name__ == '__main__':
    # print(get_amount_pharmacy_type_in_district())
    # print(get_len_title_of_pharmacy_in_district())
    # print(get_lot_of_after())
    # print(get_lot_of_between())
    # print(get_all_about_medicaments())
    # print(get_employee_from_district())
    # print(get_defect_from_manufact())
    # print(get_all_employeers())
    # print(get_medicament_with_left_join())
    # print(get_medicament_with_right_join())
    # print(get_amount_of_employeers_in_pharmacy('1'))
    # print(get_medicament_with_define_shape(['8 | Абакавир-АВС', '1 | Таблетки', '1 | Полишкина']))
    # for i in get_cheap_medicaments(['1 ', '1 | Полишкина']):
    #     print(i)
    # print(get_all_unknown_medicaments())
    print(get_all_medicament_from_manufact(1))
    pass
