import pymysql.cursors
import config
import graphics

paramstyle = "%s"


def deploy_database():
    """
     Создать нужные таблицы в базе данных
    """
    pass


def connect():
    """
     Подключение к базе данных
    """
    return pymysql.connect(
        config.db_host,
        config.db_user,
        config.db_password,
        config.db_database,
        use_unicode=True,
        charset=config.db_charset,
        cursorclass=pymysql.cursors.DictCursor)


def execute(sql, *args, commit=False):
    """
     Формат запроса:
     execute('<Запрос>', <передаваемые параметры>, <commit=True>)
    """
    db = connect()
    cur = db.cursor()
    try:
        cur.execute(sql % {"p": paramstyle}, args)
    except pymysql.err.InternalError as e:
        if sql.find('texts') == -1:
            print('Cannot execute mysql request: ' + str(e))
        return
    if commit:
        db.commit()
        db.close()
    else:
        ans = cur.fetchall()
        db.close()
        return ans


#   ========================================    ЗАДАНИЯ     ================================================


def get_all_medicament_from_pharmacy(name_of_pharmacy):
    result_of_query = execute('SELECT title_of_medicament, COUNT(title_of_medicament) as count FROM main_pharmacy '     # по итогу выводим список с названиеями всех лекарств доставленных в аптеку 
                              'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id AND '    # получаю необходимую аптеку
                              f'main_pharmacy.id = (SELECT id FROM main_pharmacy WHERE title_of_pharmacy = "{name_of_pharmacy}" ) '    # название аптеку
                              'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id '  # получаю все партии
                              'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id '   # получаю лекарства из всех партий
                              'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' # получаем все названия лекарств + их кол-во
                              'GROUP BY title_of_medicament '
                              'ORDER BY count DESC '
                              'LIMIT 5'
                              )
    return tuple(row.get('title_of_medicament').rstrip() for row in result_of_query)


def get_all_medicament_from_district(name_of_district):

    result_of_query = execute('SELECT title_of_medicament, COUNT(title_of_medicament) as count FROM main_district '     # по итогу выводим список с названиеями всех лекарств доставленных в аптеку 
                              'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id AND '
                              f'main_district.id = (SELECT id FROM main_district WHERE title_of_district = "{name_of_district}") '    # получаю необходимую аптеку
                              'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id '    # получаю необходимую аптеку
                              'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id '  # получаю все партии
                              'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id '   # получаю лекарства из всех партий
                              'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' # получаем все названия лекарств + их кол-во
                              'GROUP BY title_of_medicament '
                              'ORDER BY count DESC'
                              )
    return tuple(row.get('title_of_medicament').rstrip() for row in result_of_query[:5])


def get_all_pharmacy_from_district(name_of_district):
    result_of_query = execute('SELECT title_of_type, COUNT(title_of_type) as count FROM main_district '     # по итогу выводим список с названиеями всех лекарств доставленных в аптеку 
                              'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id AND '
                              f'main_district.id = (SELECT id FROM main_district WHERE title_of_district = "{name_of_district}") '    # получаю необходимую аптеку
                              'INNER JOIN main_type ON main_type.id = main_pharmacy.id_of_type_id '
                              'GROUP BY title_of_type '
                              'ORDER BY count DESC'
                              )
    return tuple(row.get('title_of_type') + ': ' + str(row.get('count')) for row in result_of_query)


def get_all_comebacks_from_manufacturer(name_of_manufacturer):
    result_of_query = execute('SELECT SUM(main_lot.price_manufacturer), COUNT(main_lot.defect) FROM main_manufacturer '     # по итогу выводим список с названиеями всех лекарств доставленных в аптеку 
                              'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id AND '
                              f'main_manufacturer.id = (SELECT id FROM main_manufacturer WHERE title_of_manufacturer = "{name_of_manufacturer}") '    # получаю необходимую аптеку
                              'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id WHERE defect="1" '
                              )
    return tuple('Сумма: ' + str(row.get('SUM(main_lot.price_manufacturer)')) + ', Количество возвратов: ' + str(row.get('COUNT(main_lot.defect)')) + '.' for row in result_of_query)


#   ========================================    ЗАПРОСЫ     ================================================


def get_amount_pharmacy_type_in_district(main_district_id):     # получение количества типов аптек по району с ID 1 (для одномерного графика)
    query = 'SELECT main_pharmacy.id_of_type_id as id_типа, COUNT(main_pharmacy.id_of_type_id) as Количество_аптек_данного_типа ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ' \
            f'   AND main_district.id = "{main_district_id}" ' \
            'GROUP BY main_pharmacy.id_of_type_id'
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT main_pharmacy.id_of_type_id as id_типа, COUNT(main_pharmacy.id_of_type_id) as Количество_аптек_данного_типа ||' \
           'FROM main_district ||' \
           'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ||' \
           f'   AND main_district.id = "{main_district_id}" ||' \
           'GROUP BY main_pharmacy.id_of_type_id ||'.split('||'), \
           graphics.first_graphic(labels=tuple(row.get('id_типа') for row in result_of_query),
                                  values=tuple(row.get('Количество_аптек_данного_типа') for row in result_of_query))


def get_amount_of_medicaments(main_pharmacy_id):    # получение медикаментов из аптеки
    query = 'SELECT title_of_medicament AS Название_медикамента, COUNT(title_of_medicament) AS Количество_доставок FROM ' \
            '   (SELECT main_lot.id_of_medicament_id ' \
            '   FROM main_lot ' \
            '   INNER JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ' \
            '   INNER JOIN main_pharmacy ON main_pharmacy.id = main_employee.id_of_pharmacy_id ' \
            f'       AND main_pharmacy.id = "{main_pharmacy_id}") AS medicament_in_pharm ' \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = medicament_in_pharm.id_of_medicament_id ' \
            'GROUP BY title_of_medicament'
    result_of_query = execute(query)
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
    main_pharmacy_id = datefact[0][:datefact[0].find(' ')]
    query = 'SELECT lot.id, lot.datefact AS Дата_доставки, lot.count AS Количество, lot.number_of_lot AS Номер_партии, ' \
            '    lot.datestart AS Дата_изготовления, lot.datefinish AS Срок_годности, lot.price_manufacturer AS Цена_фирмы, ' \
            '    lot.price_pharmacy AS Цена_аптеки, lot.defect AS Дефект, ' \
            '    CONCAT(main_employee.second_name, " ", LEFT(main_employee.first_name, 1), ". ", LEFT(main_employee.third_name, 1), ".") AS Принявший_сотрудник '   \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}" '  \
            'INNER JOIN main_lot as lot ON lot.id_of_employee_id = main_employee.id '  \
            f'   AND lot.datefact > "{datefact[1]}" '
    result_of_query = execute(query)
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
    main_pharmacy_id = datefact[0][:datefact[0].find(' ')]
    query = 'SELECT lot.id, lot.datefact AS Дата_доставки, lot.count AS Количество, lot.number_of_lot AS Номер_партии, ' \
            '    lot.datestart AS Дата_изготовления, lot.datefinish AS Срок_годности, lot.price_manufacturer AS Цена_фирмы, ' \
            '    lot.price_pharmacy AS Цена_аптеки, lot.defect AS Дефект, ' \
            '    CONCAT(main_employee.second_name, " ", LEFT(main_employee.first_name, 1), ". ", LEFT(main_employee.third_name, 1), ".") AS Принявший_сотрудник '   \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}" '  \
            'INNER JOIN main_lot as lot ON lot.id_of_employee_id = main_employee.id '  \
            f'   AND lot.datefact BETWEEN "{datefact[1]}" AND "{datefact[2]}" '
    result_of_query = execute(query)
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


def get_defect_from_manufact(main_manufacturer_id):     # смотрим все дефекты для определенной фирмы
    query = 'SELECT name.title_of_medicament AS Название_лекарства, main_lot.reason AS Причина_возврата, ' \
            '   main_lot.datestart AS Дата_создания '  \
            'FROM main_manufacturer '  \
            'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id ' \
            f'   AND main_manufacturer.id = "{main_manufacturer_id}" '  \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ' \
            '   AND main_lot.defect = "1" ' \
            'LEFT JOIN main_name_of_medicament as name ON name.id = main_medicament.id_of_name_of_medicament_id '
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT name.title_of_medicament AS Название_лекарства, main_lot.reason AS Причина_возврата, ||' \
            '   main_lot.datestart AS Дата_создания ||'  \
            'FROM main_manufacturer ||'  \
            'INNER JOIN main_medicament ON main_medicament.id_of_manufacturer_id = main_manufacturer.id ||' \
            f'   AND main_manufacturer.id = "{main_manufacturer_id}" ||'  \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id ||' \
            '   AND main_lot.defect = "1" ||' \
            'LEFT JOIN main_name_of_medicament as name ON name.id = main_medicament.id_of_name_of_medicament_id '.split('||'), \
           graphics.third_graphic(x=tuple(row.get('Название_лекарства') for row in result_of_query),
                                  y=tuple(row.get('Причина_возврата') for row in result_of_query),
                                  z=tuple(row.get('Дата_создания') for row in result_of_query), )


def get_all_about_medicaments(sixth_querys):    # получение определенного лекарства в определенном районе
    main_district_id = sixth_querys[0][:sixth_querys[0].find(' ')]
    main_lot_id_of_medicament_id = sixth_querys[1][:sixth_querys[1].find(' ')]
    query = 'SELECT main_lot.count AS Количество_на_складе, ' \
            '       main_lot.datefinish AS Срок_годности, ' \
            '       main_lot.price_pharmacy AS Цена, ' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки '  \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
            f'   AND main_district.id = "{main_district_id}" ' \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_pharmacy.id ' \
            f'   AND main_lot.defect = "0" AND main_lot.id_of_medicament_id = "{main_lot_id_of_medicament_id}" '
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT main_lot.count AS Количество_на_складе, ||' \
           '    main_lot.datefinish AS Срок_годности, ||' \
           '    main_lot.price_pharmacy AS Цена, ||' \
           '    main_pharmacy.title_of_pharmacy AS Название_аптеки  ||'  \
           'FROM main_district ||' \
           'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ||' \
           '   AND main_district.id = "1" ||'  \
           'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_pharmacy.id ||' \
           '   AND main_lot.defect = "0" AND main_lot.id_of_medicament_id = "1" '.split('||')


def get_all_employeers(main_pharmacy_id):   # получение всех работников определенной аптеки
    query = 'SELECT main_employee.second_name AS Фамилия, ' \
            '       main_employee.first_name AS Имя, ' \
            '       main_employee.third_name AS Отчество '  \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            f'   AND main_pharmacy.id = "{main_pharmacy_id}"'
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT main_employee.second_name AS Фамилия, ||' \
           '       main_employee.first_name AS Имя, ||' \
           '       main_employee.third_name AS Отчество ||'  \
           'FROM main_pharmacy ||' \
           'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
           f'   AND main_pharmacy.id = "{main_pharmacy_id}" '.split('||')


def get_medicament_with_right_join(worker):    # получаем все лекарства принимаемые каким-то одним работником
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
            'RIGHT JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ' \
            f'   AND main_employee.id = "{worker}" ' \
            'GROUP BY main_lot.id ' \
            'HAVING MIN(main_lot.id) - 1 < main_lot.id '
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT main_name_of_medicament.title_of_medicament AS Название_лекарства, ||' \
           '       main_lot.datefact AS Дата_приема ||'  \
           'FROM main_lot ||' \
           'RIGHT JOIN main_employee ON main_employee.id = main_lot.id_of_employee_id ||' \
           f'   AND main_employee.id = "{worker}" ||' \
           'RIGHT JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id ||' \
           'RIGHT JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id '.split('||')


def get_all_employeers_in_db():
    query = 'SELECT id,' \
            '       first_name AS Имя,' \
            '       second_name AS Фамилия, ' \
            '       third_name AS Отчество ' \
            'FROM main_employee'
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT id, ||' \
           '       first_name AS Имя, ||' \
           '       second_name AS Фамилия, ||' \
           '       third_name AS Отчество ||' \
           'FROM main_employee'.split('||')


def get_medicament_with_define_shape(tenth_query):
    main_name_of_medicament_id = tenth_query[0][:tenth_query[0].find(' ')]
    main_shape_id = tenth_query[1][:tenth_query[1].find(' ')]
    main_district_id = tenth_query[2][:tenth_query[2].find(' ')]
    query = 'SELECT ' \
            '       main_lot.price_pharmacy AS Цена, ' \
            '       main_lot.datefact AS Срок_годности, ' \
            '       main_lot.count AS Количество, ' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
            '       main_pharmacy.phone_of_pharmacy AS Телефон, ' \
            '       main_pharmacy.address_of_pharmacy AS Адрес ' \
            'FROM main_pharmacy ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            f'   AND main_pharmacy.id_of_district_id = {main_district_id} ' \
            'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ' \
            '   AND main_lot.defect = "0" ' \
            f'INNER JOIN main_medicament ON main_medicament.id_of_shape_id = {main_shape_id} ' \
            f'  AND main_medicament.id_of_name_of_medicament_id = {main_name_of_medicament_id}'
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT ' \
            '       main_lot.price_pharmacy AS Цена, ||' \
            '       main_lot.datefact AS Срок_годности, ||' \
            '       main_lot.count AS Количество, ||' \
            '       main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
            '       main_pharmacy.phone_of_pharmacy AS Телефон, ||' \
            '       main_pharmacy.address_of_pharmacy AS Адрес, ||' \
            'FROM main_pharmacy ||' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
            f'   AND main_pharmacy.id_of_district_id = {main_district_id} ||' \
            'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id ||' \
            '   AND main_lot.defect = "0" ||' \
            f'INNER JOIN main_medicament ON main_medicament.id_of_shape_id = {main_shape_id} ||' \
            f'  AND main_medicament.id_of_name_of_medicament_id = {main_name_of_medicament_id}'.split('||')


def get_amount_of_employeers_in_pharmacy(main_district_id):
    query = 'SELECT main_pharmacy.title_of_pharmacy AS Название_аптеки, ' \
            '       COUNT(main_employee.id) AS Количество_работников ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ' \
            f'   AND main_district.id = {main_district_id} ' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ' \
            'GROUP BY main_pharmacy.title_of_pharmacy '
    result_of_query = execute(query)
    return result_of_query, \
           'SELECT main_pharmacy.title_of_pharmacy AS Название_аптеки, ||' \
            '       COUNT(main_employee.id) AS Количество_работников ||' \
            'FROM main_district ||' \
            'INNER JOIN main_pharmacy ON main_pharmacy.id_of_district_id = main_district.id ||' \
            f'   AND main_district.id = {main_district_id} ||' \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id ||' \
            'GROUP BY main_pharmacy.title_of_pharmacy '.split('||')


def get_cheap_medicaments(get_all_data):
    main_district_id = get_all_data[1][:get_all_data[1].find(' ')]
    main_medicament_id = get_all_data[0][:get_all_data[0].find(' ')]
    # подказпрос который возвращает все найденные лекарства в данном регионе
    sub_query = 'SELECT ' \
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
    query = 'SELECT Количество_препарата,' \
            '       Цена_препарата, ' \
            '       Название_аптеки ' \
            f'FROM ({sub_query}) AS list_medicaments ' \
            'GROUP BY list_medicaments.Название_аптеки '
    result_of_query = execute(query)
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



def sum_all_methods_for_querys(get_all_data):

    return {'<h3>1.Вывод всех типов аптек (и количество аптек) по заданному району.<br>(первый внутренний запрос по внешнему ключу)</h3>'
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

            '<h3>5.Получение всех возвратов и их причин по определенной фирме<br>(первый внутренне симметричный запрос + левое соединение)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('fifth_querys')[0]} </div>":
                get_defect_from_manufact(get_all_data.get('fifth_querys')[0][:get_all_data.get('fifth_querys')[0].find(' ')]),

            '<h3>6.Получение всего об определенном лекартсве по району (без дефекта)<br>(второй внутренне симметричный запрос)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{', '.join(get_all_data.get('sixth_querys'))} </div>":
                get_all_about_medicaments(get_all_data.get('sixth_querys')),

            '<h3>7.Получение всех работников<br>(третий внутренне симметричный запрос)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('eigth_querys')[0]} </div>":
                get_all_employeers(get_all_data.get('seventh_querys')[0][:get_all_data.get('seventh_querys')[0].find(' ')]),

            '<h3>8.Получение всех лекарств путем правого соединения<br>(правое внешнее соединение)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('eigth_querys')[0]} </div>":
                get_medicament_with_right_join(get_all_data.get('eigth_querys')[0][:get_all_data.get('eigth_querys')[0].find(' ')]),
            '<h3>9.Получение всех сотрудников всех аптек<br>(итоговый запрос без условия)</h3>':
                get_all_employeers_in_db(),

            '<h3>10.Получение всех лекарст с определенной формой,<br>по определенному району<br>(итоговый запрос с условия на данные)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{', '.join(get_all_data.get('tenth_querys'))} </div>":
                get_medicament_with_define_shape(get_all_data.get('tenth_querys')),

            '<h3>11.Получение всех сотрудников всех аптек по району<br>(итоговый запрос с условием на группы)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{get_all_data.get('eleventh_querys')[0]} </div>":
                get_amount_of_employeers_in_pharmacy(get_all_data.get('eleventh_querys')[0][:get_all_data.get('eleventh_querys')[0].find(' ')]),

            '<h3>12.Получение всех дешевых препаратав по району<br>(итоговый запрос без с условие на группы и данные)</h3>'
            f"<div class=\"alert alert-primary\">Исходные данные:<br>{', '.join(get_all_data.get('twelveth_querys'))} </div>":
                get_cheap_medicaments(get_all_data.get('twelveth_querys')),
            }


if __name__ == '__main__':
    # print(get_amount_pharmacy_type_in_district())
    # print(get_len_title_of_pharmacy_in_district())
    # print(get_lot_of_after())
    # print(get_lot_of_between())
    # print(get_all_about_medicaments())
    # print(get_defect_from_manufact())
    # print(get_all_employeers())
    # print(get_medicament_with_left_join())
    # print(get_medicament_with_right_join())
    # print(get_amount_of_employeers_in_pharmacy('1'))
    # print(get_medicament_with_define_shape(['8 | Абакавир-АВС', '1 | Таблетки', '1 | Полишкина']))
    # for i in get_cheap_medicaments(['1 ', '1 | Полишкина']):
    #     print(i)
    pass
