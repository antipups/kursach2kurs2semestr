"""

    Файл создан для функций проверки вводимых данных;

"""


def pharmacy(**dict_of_post):
    number_of_pharmacy, title_of_pharmacy, address_of_pharmacy, id_of_district, phone_of_pharmacy = \
        dict_of_post.get('number_of_pharmacy'), dict_of_post.get('title_of_pharmacy'), dict_of_post.get('address_of_pharmacy'), dict_of_post.get('id_of_district'), dict_of_post.get('phone_of_pharmacy'),
    if len(number_of_pharmacy) > 0 and number_of_pharmacy.isdigit() and (int(number_of_pharmacy) < 0 or int(number_of_pharmacy) > 1000000):
        return 'number_of_pharmacy'
    if len(title_of_pharmacy) > 15 or len(title_of_pharmacy) == 0 or any(map(lambda x: x.isdigit(), title_of_pharmacy)):
        return 'title_of_pharmacy'
    if len(address_of_pharmacy) == 0 or len(address_of_pharmacy) > 12:
        return 'address_of_pharmacy'
    if len(phone_of_pharmacy) == 0 or len(phone_of_pharmacy) > 10 or phone_of_pharmacy.isdigit() is False:
        return 'phone_of_pharmacy'
    if id_of_district is None:
        return 'id_of_district'
    return True


