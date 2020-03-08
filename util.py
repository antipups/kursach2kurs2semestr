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


def get_amount_pharmacy_type_in_district():     # получение количества типов аптек по району с ID 1 (для одномерного графика)
    query = 'SELECT main_pharmacy.id_of_type_id as id_типа, COUNT(main_pharmacy.id_of_type_id) as Количество_аптек_данного_типа ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ' \
            '   AND main_district.id = "1" ' \
            'GROUP BY main_pharmacy.id_of_type_id'
    result_of_query = execute(query)
    return result_of_query, tuple((row.get('id_типа'), row.get('Количество_аптек_данного_типа')) for row in result_of_query), \
           'SELECT main_pharmacy.id_of_type_id as id_типа, COUNT(main_pharmacy.id_of_type_id) as Количество_аптек_данного_типа ||' \
           'FROM main_district ||' \
           'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ||' \
           '   AND main_district.id = "1" ||' \
           'GROUP BY main_pharmacy.id_of_type_id ||'.split('||'), \
           graphics.first_graphic(labels=tuple(row.get('id_типа') for row in result_of_query),
                                  values=tuple(row.get('Количество_аптек_данного_типа') for row in result_of_query))



def get_len_title_of_pharmacy_in_district():    # получение длин названий аптек по району с ID 1 (для двумерного графика)
    query = 'SELECT main_pharmacy.title_of_pharmacy, ROUND(LENGTH(main_pharmacy.title_of_pharmacy) / 2) as len ' \
            'FROM main_district ' \
            'INNER JOIN main_pharmacy ON main_district.id = main_pharmacy.id_of_district_id ' \
            '   AND main_district.id = "1" '
    result_of_query = execute(query)
    return result_of_query, tuple((row.get('title_of_pharmacy'), row.get('len')) for row in result_of_query), query


def get_lot_of_after():    # получение партий после определенного числа
    query = 'SELECT main_lot.id '   \
            'FROM main_medicament '  \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id '  \
            '   AND main_medicament.id = "1" '  \
            '   AND datefact > "2020-02-13" '
    result_of_query = execute(query)
    return result_of_query, query


def get_lot_of_between():    # получение партий после определенного числа
    query = 'SELECT main_lot.id '  \
            'FROM main_medicament '  \
            'INNER JOIN main_lot ON main_lot.id_of_medicament_id = main_medicament.id '  \
            '   AND main_lot.datefact BETWEEN "2020-02-13" AND "2020-02-17"'
    result_of_query = execute(query)
    return result_of_query, query


def get_all_pharmacy():     # для 3д графика
    query = 'SELECT main_lot.datefact, main_lot.count, main_name_of_medicament.title_of_medicament '  \
            'FROM main_lot '  \
            'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id '  \
            'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id'
    result_of_query = execute(query)
    return result_of_query, query


def get_all_medicaments():
    query = 'SELECT main_name_of_medicament.title_of_medicament '  \
            'FROM main_name_of_medicament '  \
            'INNER JOIN main_medicament ON main_medicament.id_of_name_of_medicament_id = main_name_of_medicament.id '
    result_of_query = execute(query)
    return result_of_query, query


def get_all_employeers():
    query = 'SELECT main_employee.second_name , main_employee.first_name , main_employee.third_name '  \
            'FROM main_pharmacy '  \
            'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id '
    result_of_query = execute(query)
    return result_of_query, query


def get_medicament_with_left_join():
    query = 'SELECT * '  \
            'FROM main_medicament '  \
            'LEFT JOIN main_name_of_medicament ON main_medicament.id_of_name_of_medicament_id = main_name_of_medicament.id '
    result_of_query = execute(query)
    return result_of_query, query


def get_medicament_with_right_join():
    query = 'SELECT * '  \
            'FROM main_name_of_medicament '  \
            'RIGHT JOIN main_medicament ON main_medicament.id_of_name_of_medicament_id = main_name_of_medicament.id '
    result_of_query = execute(query)
    return result_of_query, query


def sum_all_methods_for_querys():
    return {'get_amount_pharmacy_type_in_district': get_amount_pharmacy_type_in_district(),
            'get_len_title_of_pharmacy_in_district': get_len_title_of_pharmacy_in_district(),
            'get_lot_of_after': get_lot_of_after(),
            'get_lot_of_between': get_lot_of_between(),
            'get_all_pharmacy': get_all_pharmacy(),
            'get_all_medicaments': get_all_medicaments(),
            'get_all_employeers': get_all_employeers(),
            'get_medicament_with_left_join': get_medicament_with_left_join(),
            'get_medicament_with_right_join': get_medicament_with_right_join(),
            }


if __name__ == '__main__':
    # print(get_amount_pharmacy_type_in_district())
    # print(get_len_title_of_pharmacy_in_district())
    # print(get_lot_of_after())
    # print(get_lot_of_between())
    # print(get_all_pharmacy())
    # print(get_all_medicaments())
    # print(get_all_employeers())
    # print(get_medicament_with_left_join())
    # print(get_medicament_with_right_join())
    pass
