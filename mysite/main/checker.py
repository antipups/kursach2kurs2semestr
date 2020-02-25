"""

    Файл создан для функций проверки вводимых данных;

"""
import re
import datetime


def pharmacy(**dict_of_post):
    number_of_pharmacy, title_of_pharmacy, address_of_pharmacy, id_of_district, phone_of_pharmacy = \
        dict_of_post.get('number_of_pharmacy'), dict_of_post.get('title_of_pharmacy'), dict_of_post.get('address_of_pharmacy'), dict_of_post.get('id_of_district'), dict_of_post.get('phone_of_pharmacy'),
    if len(number_of_pharmacy) > 0 and number_of_pharmacy.isdigit() and (int(number_of_pharmacy) < 0 or int(number_of_pharmacy) > 1000000):
        return
    if len(title_of_pharmacy) > 15 or len(title_of_pharmacy) == 0 or any(map(lambda x: x.isdigit(), title_of_pharmacy)):
        return
    if len(address_of_pharmacy) == 0 or len(address_of_pharmacy) > 12:
        return
    if len(phone_of_pharmacy) == 0 or len(phone_of_pharmacy) > 10 or phone_of_pharmacy.isdigit() is False:
        return
    if id_of_district is None:
        return
    return True


def country(**dict_of_post):
    if len(dict_of_post.get('title_of_country')) == 0 or len(dict_of_post.get('title_of_country')) > 3 or any(map(lambda x: x.isdigit(), dict_of_post.get('title_of_country'))) is True:
        return
    return True


def manufacturer(**dict_of_post):
    title_of_manufacturer, address_of_manufacturer, email_of_manufacturer, year_of_manufacturer = \
        dict_of_post.get('title_of_manufacturer'), dict_of_post.get('address_of_manufacturer'), dict_of_post.get('email_of_manufacturer'), dict_of_post.get('year_of_manufacturer')
    if len(title_of_manufacturer) == 0 or len(title_of_manufacturer) > 30 or any(map(lambda x: x.isdigit(), title_of_manufacturer)):
        return
    if dict_of_post.get('id_of_country') is None:
        return
    if len(address_of_manufacturer) == 0 or len(address_of_manufacturer) > 70:
        return
    if len(email_of_manufacturer) == 0 or len(email_of_manufacturer) > 30:
        return
    if (len(year_of_manufacturer) == 0 or len(year_of_manufacturer) > 4) and year_of_manufacturer.isdigit() is False and int(year_of_manufacturer) > 2020:
        return
    return True


def shape(**dict_of_post):
    if len(dict_of_post.get('title_of_shape')) == 0 or len(dict_of_post.get('title_of_shape')) > 15 or any(map(lambda x: x.isdigit(), dict_of_post.get('title_of_shape'))):
        return
    return True


def pharma_group(**dict_of_post):
    if len(dict_of_post.get('title_of_pharma_group')) == 0 or len(dict_of_post.get('title_of_pharma_group')) > 15 or any(map(lambda x: x.isdigit(), dict_of_post.get('title_of_pharma_group'))):
        return
    return True


def medicament(**dict_of_post):
    comments, bar_code,  = dict_of_post.get('comments'), dict_of_post.get('bar_code')
    if dict_of_post.get('id_of_shape') is None or dict_of_post.get('id_of_pharma_group') is None or dict_of_post.get('id_of_manufacturer') is None or dict_of_post.get('id_of_name_of_medicament') is None :
        return
    if len(comments) == 0:
        return
    if len(bar_code) == 0 or len(bar_code) > 100:
        return
    return True


def district(**dict_of_post):
    if len(dict_of_post.get('title_of_district')) == 0 or len(dict_of_post.get('title_of_district')) > 15 or any(map(lambda x: x.isdigit(), dict_of_post.get('title_of_district'))):
        return
    return True


def employee(**dict_of_post):
    if dict_of_post.get('id_of_pharmacy') is None:
        return
    first_name, second_name, third_name = dict_of_post.get('first_name'), dict_of_post.get('second_name'), dict_of_post.get('third_name')
    for row in first_name, second_name, third_name:
        if len(row) == 0 or len(row) > 20 or any(map(lambda x: x.isdigit(), row)):
            return
    return True


def lot(**dict_of_post):
    if dict_of_post.get('id_of_medicament') is None or dict_of_post.get('id_of_employee') is None:
        return
    datefact, count, number_of_lot, datestart, datefinish, price_manufacturer, price_pharmacy, defect, reason = \
        dict_of_post.get('datefact'), dict_of_post.get('count'), dict_of_post.get('number_of_lot'), dict_of_post.get('datestart'), dict_of_post.get('datefinish'), \
        dict_of_post.get('price_manufacturer'), dict_of_post.get('price_pharmacy'), dict_of_post.get('defect'), dict_of_post.get('reason')
    try:
        datefact, datestart, datefinish = datetime.date(int(datefact[:4]), int(datefact[5:7]), int(datefact[-2:])), \
                                          datetime.date(int(datestart[:4]), int(datestart[5:7]), int(datestart[-2:])), \
                                          datetime.date(int(datefinish[:4]), int(datefinish[5:7]), int(datefinish[-2:]))
        one_day = datetime.timedelta(days=1)    # переменная разность, чтоб регулировать даты
        if datefinish - datestart < one_day or datefinish - datefact < one_day or datefact - datestart < one_day:
            return
    except:
        return
    if len(count) == 0 or count.isdigit() is False:
        return
    if len(number_of_lot) == 0 or len(number_of_lot) > 4 or number_of_lot.isdigit() is False:
        return
    if len(price_pharmacy) == 0 or len(price_pharmacy) > 4 or price_pharmacy.isdigit() is False:
        return
    if len(price_manufacturer) == 0 or len(price_manufacturer) > 4 or price_manufacturer.isdigit() is False:
        return
    if defect != '0' and defect != '1':
        return
    if len(reason) == 0 and defect == '1':
        return
    return True


def name_of_medicament(**dict_of_post):
    if len(dict_of_post.get('title_of_medicament')) == 0 or len(dict_of_post.get('title_of_medicament')) > 20 or any(map(lambda x: x.isdigit(), dict_of_post.get('title_of_medicament'))):
        return
    return True


def type(**dict_of_post):
    if len(dict_of_post.get('title_of_type')) == 0 or len(dict_of_post.get('title_of_type')) > 15 or any(map(lambda x: x.isdigit(), dict_of_post.get('title_of_type'))):
        return
    return True
