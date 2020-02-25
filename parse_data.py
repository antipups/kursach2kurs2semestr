import random
import re
import requests
import pymysql
import xlrd, xlwt


connect = pymysql.connect(host='localhost', user='root', password='', db="school_work")
cursor = connect.cursor()


# ниже парс СТРАН
# html = requests.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2').text
# ls_of_country = re.findall(r'data-sort-value=\"[^\"]*', html)
#
# for i in ls_of_country:
#     country = i[i.rfind('\"') + 1:i.rfind('\"') + 4].upper()
#     try:
#         cursor.execute(f'INSERT INTO main_country (title_of_country) VALUES ("{country}")')
#         connect.commit()
#     except:
#         continue


# ниже парс улиц
# html = requests.get('https://ru.wikipedia.org/wiki/Улицы_Донецка').text
# html = html[html.find('<p>Позже улицы были переименованы:') + 34:html.find('<h2>')]
# ls_of_district = re.findall(r'линия[^<]*', html)
# with open('Улицы.txt', 'w', encoding='utf-8') as f:
#     for i in ls_of_district[:-1]:
#         street = i[i.rfind('—') + 2:].replace('улица', '').strip()
#         f.write(street + '\n')


# Ниже парс фирм
# rb = xlrd.open_workbook('C:\\Users\\kurku\\PycharmProjects\\parse_for_five\\books.xls',
#                         formatting_info=True)
# sheet = rb.sheet_by_index(0)
# for row in range(4337):
#
#     html = requests.get('http://www.yopmail.com/ru/email-generator.php',).text
#     url = html[html.find('onmouseup="this.select();" type="text" value="') + 46:]
#     email = url[:url.find('"')].replace('&#64;', '@')
#     year = random.randint(1990, 2020)
#     name = sheet.row_values(row)[0]
#     address = sheet.row_values(row)[2]


# парс Лекарств

# with open('medicaments.txt', 'w') as f:
#     for j in 'https://www.rlsnet.ru/tn_alf_letter_c0.htm', 'https://www.rlsnet.ru/tn_alf_letter_c1.htm', 'https://www.rlsnet.ru/tn_alf_letter_c2.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_c3.htm', 'https://www.rlsnet.ru/tn_alf_letter_c4.htm', 'https://www.rlsnet.ru/tn_alf_letter_c5.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_c6.htm', 'https://www.rlsnet.ru/tn_alf_letter_c7.htm', 'https://www.rlsnet.ru/tn_alf_letter_c8.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_c9.htm', 'https://www.rlsnet.ru/tn_alf_letter_ca.htm', 'https://www.rlsnet.ru/tn_alf_letter_cb.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_cc.htm', 'https://www.rlsnet.ru/tn_alf_letter_cd.htm', 'https://www.rlsnet.ru/tn_alf_letter_ce.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_cf.htm', 'https://www.rlsnet.ru/tn_alf_letter_d0.htm', 'https://www.rlsnet.ru/tn_alf_letter_d1.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_d2.htm', 'https://www.rlsnet.ru/tn_alf_letter_d3.htm', 'https://www.rlsnet.ru/tn_alf_letter_d4.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_d5.htm', 'https://www.rlsnet.ru/tn_alf_letter_d6.htm', 'https://www.rlsnet.ru/tn_alf_letter_d7.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_d8.htm', 'https://www.rlsnet.ru/tn_alf_letter_d9.htm', 'https://www.rlsnet.ru/tn_alf_letter_da.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_db.htm', 'https://www.rlsnet.ru/tn_alf_letter_dc.htm', 'https://www.rlsnet.ru/tn_alf_letter_de.htm',\
#              'https://www.rlsnet.ru/tn_alf_letter_df.htm', :
#         html = requests.get(j).text
#         html = html[html.find('<div class="alphabet__raspor" id="' + j[36:38] + 'e0"></div>') + 46:]
#         html = html[:html.find('<!--noindex--><div class="j-banner__group noprint"></div><!--/noindex-->')]
#         list_of_pharmacy = re.findall(r'\">[^<]*', html)
#         for i in tuple(x[2:] for x in list_of_pharmacy if len(x) > 2):
#             if i == 'Аптечка':
#                 break
#             if len(i) <= 20:
#                 f.write(i + '\n')
#


