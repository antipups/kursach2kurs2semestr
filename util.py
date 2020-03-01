import pymysql.cursors
import config

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


def get_all_medicament_from_pharmacy(name_of_pharmacy):
    result_of_query = execute('SELECT title_of_medicament, COUNT(title_of_medicament) as count FROM main_pharmacy '     # по итогу выводим список с названиеями всех лекарств доставленных в аптеку 
                              'INNER JOIN main_employee ON main_employee.id_of_pharmacy_id = main_pharmacy.id AND '    # получаю необходимую аптеку
                              f'main_pharmacy.id = (SELECT id FROM main_pharmacy WHERE title_of_pharmacy = "{name_of_pharmacy}" ) '    # название аптеку
                              'INNER JOIN main_lot ON main_lot.id_of_employee_id = main_employee.id '  # получаю все партии
                              'INNER JOIN main_medicament ON main_medicament.id = main_lot.id_of_medicament_id '   # получаю лекарства из всех партий
                              'INNER JOIN main_name_of_medicament ON main_name_of_medicament.id = main_medicament.id_of_name_of_medicament_id ' # получаем все названия лекарств + их кол-во
                              'GROUP BY title_of_medicament '
                              'ORDER BY count DESC'
                              )
    return tuple(row.get('title_of_medicament').rstrip() for row in result_of_query[:5])


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
                              # 'GROUP BY main_lot.defect'
                              )
    return tuple('Сумма: ' + str(row.get('SUM(main_lot.price_manufacturer)')) + ', Количество возвратов: ' + str(row.get('COUNT(main_lot.defect)')) + '.' for row in result_of_query)