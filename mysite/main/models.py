from django.db import models
import datetime
# from PIL import Image


################################################################

# ____________________________ФИРМА___________________________ #

################################################################


class Country(models.Model):
    """
        Таблица с странами
    """
    title_of_country = models.CharField(max_length=3, unique=True)

    @staticmethod
    def readable():
        return 'id', 'title_of_country'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_country

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_country', 'РОС', 3, 'text', 'required', 'Введите сокращение (до 3-ёх символов)', '[A-zА-я]{1,3}')}


class Reason(models.Model):
    """
        Таблица с причинами
    """
    title_of_reason = models.CharField(max_length=100, unique=True)

    @staticmethod
    def readable():
        return 'id', 'title_of_reason'

    @staticmethod
    def readable_rus():
        return 'id', 'Причина'

    def getter(self):
        return self.id, self.title_of_reason

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_reason', 'Поломанная упаковка', 100, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 100 символов', '[A-zА-я]{1,100}')}


class Manufacturer(models.Model):
    """
        Таблица с фирмами, внешние ключи:
            Country (страны).
    """
    title_of_manufacturer = models.CharField(max_length=30)
    id_of_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address_of_manufacturer = models.CharField(max_length=30)
    email_of_manufacturer = models.CharField(max_length=30)
    year_of_manufacturer = models.IntegerField()

    @staticmethod
    def readable():
        return 'id', 'title_of_manufacturer', 'id_of_country', 'address_of_manufacturer', \
               'email_of_manufacturer', 'year_of_manufacturer'

    @staticmethod
    def readable_rus():
        return 'id', 'Название', 'Страна', 'Адрес', 'E-mail', 'Год основания'

    def getter(self):
        return self.id, self.title_of_manufacturer, self.id_of_country.title_of_country, self.address_of_manufacturer, self.email_of_manufacturer, self.year_of_manufacturer

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_manufacturer', 'ООО АвтоРог', 30, 'text', 'required', 'Введите меньше 30 символов<br>и только буквы', '[A-zА-я]{1,30}'),
                'Адрес': ('address_of_manufacturer', 'Пушкина 16/2', 30, 'text', 'required', 'Введите меньше 30 символов', '.{1,30}'),
                'E-mail': ('email_of_manufacturer', 'rog@gmail.com', 30, 'email', 'required', 'Нет знака @', '.{1,30}'),
                'Год': ('year_of_manufacturer', '2001', 4, 'text', 'required', 'Введите значение<br>больше 1900, и меньше 2020', '((19[0-9]{2})|(20(([0-1][0-9])|20)))')}


################################################################

# __________________________ЛЕКАРСТВА_________________________ #

################################################################


class Shape(models.Model):
    """
        Таблица форм выпуска
    """
    title_of_shape = models.CharField(max_length=15, unique=True)

    @staticmethod
    def readable():
        return 'id', 'title_of_shape'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_shape

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_shape', 'Таблетки', 15, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 15 символов', '[A-zА-я]{1,15}')}


class Pharma_group(models.Model):
    """
        Таблица фармакалогических групп
    """
    title_of_pharma_group = models.CharField(max_length=20, unique=True)

    @staticmethod
    def readable():
        return 'id', 'title_of_pharma_group'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_pharma_group

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_pharma_group', 'Калиев каналов актив', 20, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 20 символов', '[A-zА-я]{1,20}')}


class Name_of_medicament(models.Model):
    """
        Таблица названия медикаментов
    """
    title_of_medicament = models.CharField(max_length=20, unique=True)

    @staticmethod
    def readable():
        return 'id', 'title_of_medicament'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_medicament

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_medicament', 'Анадрол', 20, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 20 символов', '[A-zА-я]{1,20}')}


class Medicament(models.Model):
    """
        Таблица медикаментов, внешние ключи:
            Shape (форма выпуска);
            Pharma_group (фармак. группа);
            Manufacturer (фирма).
    """
    id_of_name_of_medicament = models.ForeignKey(Name_of_medicament, on_delete=models.CASCADE)
    id_of_shape = models.ForeignKey(Shape, on_delete=models.CASCADE)
    id_of_pharma_group = models.ForeignKey(Pharma_group, on_delete=models.CASCADE)
    comments = models.TextField()
    bar_code = models.TextField()
    id_of_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    @staticmethod
    def readable():
        return 'id', 'id_of_name_of_medicament', 'id_of_shape', 'id_of_pharma_group',\
               'comments', 'bar_code', 'id_of_manufacturer'

    @staticmethod
    def readable_rus():
        return 'id', 'Название', 'Форма выпуска', 'Фармакологическая группа',\
               'Инструкция', 'Штрих-код', 'Фирма'

    def getter(self):
        return self.id, self.id_of_name_of_medicament.title_of_medicament, self.id_of_shape.title_of_shape, self.id_of_pharma_group.title_of_pharma_group, self.comments, self.bar_code, self.id_of_manufacturer.title_of_manufacturer

    @staticmethod
    def get_attr():
        return {'Инструкция': ('comments', 'Принимать после еды 3 раза в день.', 100, 'text', 'required', 'Длина меньше 100 символов', '.{1,100}')}

################################################################

# ____________________________АПТЕКИ__________________________ #

################################################################


class Type(models.Model):
    """
        Таблица типов собственности
    """
    title_of_type = models.CharField(max_length=15, unique=True)

    @staticmethod
    def readable():
        return 'id', 'title_of_type'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_type

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_type', 'Частная', 15, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 15 символов', '[A-zА-я]{1,15}')}


class District(models.Model):
    """
        Таблица районов
    """
    title_of_district = models.CharField(max_length=15, unique=True, )

    @staticmethod
    def readable():
        return 'id', 'title_of_district'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_district

    @staticmethod
    def get_attr():
        return {'Название': ('title_of_district', 'Кировский', 15, 'text', 'required', 'Введите корректное название района и <br>длина меньше 15 символов', '[A-zА-я]{0,15}')}


class Pharmacy(models.Model):
    """
        Таблица аптек, внешние ключи:
            District (районы).
    """

    number_of_pharmacy = models.IntegerField()
    title_of_pharmacy = models.CharField(max_length=15)
    id_of_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    address_of_pharmacy = models.CharField(max_length=12)
    id_of_district = models.ForeignKey(District, on_delete=models.CASCADE)
    phone_of_pharmacy = models.CharField(max_length=10)

    @staticmethod
    def readable():
        return 'id', 'number_of_pharmacy', 'title_of_pharmacy', 'id_of_type',\
               'address_of_pharmacy', 'id_of_district', 'phone_of_pharmacy'

    @staticmethod
    def readable_rus():
        return 'id', 'Номер', 'Название', 'Тип собственности', 'Адрес', 'Район', 'Телефон'

    def getter(self):
        return self.id, self.number_of_pharmacy, self.title_of_pharmacy, self.id_of_type.title_of_type, self.address_of_pharmacy, self.id_of_district.title_of_district, self.phone_of_pharmacy

    @staticmethod
    def get_attr():
        return {'Номер': ('number_of_pharmacy', '0123456789', 100, 'text', 'required', 'Допускаются только цифры и<br>длина меньше 100 символов', '[0-9]{1,100}'),
                'Название': ('title_of_pharmacy', 'Черника', 15, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 15', '[A-zА-я]{1,15}'),
                'Адрес': ('address_of_pharmacy', 'Пушкина дом 16', 15, 'text', 'required', 'Длина меньше 15 символов', '.{1,15}'),
                'Телефон': ('phone_of_pharmacy', '0123456789', 10, 'text', 'required', 'Допускаются только цифры и<br>длина меньше 10 символов', '[0-9]{1,10}')}


################################################################

# ____________________________ПАРТИЯ__________________________ #

################################################################


class Employee(models.Model):
    """
        Таблица работника, внешние ключи:
            Pharmacy (аптека).
    """
    id_of_pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    third_name = models.CharField(max_length=20)

    @staticmethod
    def readable():
        return 'id', 'id_of_pharmacy', 'first_name', 'second_name', 'third_name',

    @staticmethod
    def readable_rus():
        return 'id', 'Аптека', 'Имя', 'Фамилия', 'Отчество',

    def getter(self):
        return self.id, self.id_of_pharmacy.title_of_pharmacy, self.first_name, self.second_name, self.third_name

    @staticmethod
    def get_attr():
        return {'Фамилия': ('second_name', 'Пупкин', 20, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 20 символов', '[A-zА-я]{1,20}'),
                'Имя': ('first_name', 'Василий', 20, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 20 символов', '[A-zА-я]{1,20}'),
                'Отчество': ('third_name', 'Васильевич', 20, 'text', 'required', 'Допускаются только буквы и<br>длина меньше 20 символов', '[A-zА-я]{1,20}')}


class Lot(models.Model):
    """
        Таблица партий, внешние ключи:
            Employee (работник).
            Medicament (лекарство)
    """
    id_of_medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    datefact = models.DateField()
    count = models.IntegerField()
    number_of_lot = models.IntegerField()
    datestart = models.DateField()
    datefinish = models.DateField()
    price_manufacturer = models.IntegerField()
    price_pharmacy = models.IntegerField()
    id_of_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    defect = models.BooleanField(default=False)
    id_of_reason = models.ForeignKey(Reason, on_delete=models.CASCADE, default=None)

    @staticmethod
    def readable():
        return 'id', 'id_of_medicament', 'datefact', 'count', 'number_of_lot', 'datestart', 'datefinish', \
               'price_manufacturer', 'price_pharmacy', 'id_of_employee', 'defect', 'id_of_reason'

    @staticmethod
    def readable_rus():
        return 'id', 'Лекарство', 'Дата доставки', 'Кол-во упаковок', 'Номер', 'Дата выпуска', 'Дата срока годности', \
               'Цена(Фирма)', 'Цена(Аптека)', 'Работник', 'Дефект', 'Причина возврата'

    def getter(self):
        return self.id, self.id_of_medicament.id_of_name_of_medicament.title_of_medicament, self.datefact.strftime('%Y/%m/%d'), self.count, self.number_of_lot, self.datestart.strftime('%Y/%m/%d') , self.datefinish.strftime('%Y/%m/%d'), \
               self.price_manufacturer, self.price_pharmacy, \
               ' '.join((self.id_of_employee.second_name, self.id_of_employee.first_name[0] + '. ', self.id_of_employee.third_name[0] + '.')), \
               self.defect, self.id_of_reason.title_of_reason

    @staticmethod
    def get_attr():
        return {'Дата доставки': ('datefact', '23.03.2012', 15, 'date', 'required', 'Допускаются дата > даты изготовления<br>но меньше сегодняшней', '.{1,15}'),
                'Кол-во упаковок': ('count', '1234567890', 10, 'text', 'required', 'Допускаются только цифры и<br>длина меньше 10 символов', '[0-9]{1,10}'),
                'Номер': ('number_of_lot', '4321', 4, 'text', 'required', 'Допускаются только цифры и<br>длина меньше 4 символов', '[0-9]{1,4}'),
                'Дата выпуска': ('datestart', '20.03.2012', 15, 'date', 'required', 'Допускаются только цифры и<br>длина меньше 20 символов', '.{1,15}'),
                'Дата срока годности': ('datefinish', '25.03.2012', 15, 'date', 'required', 'Допускаются только цифры и<br>длина меньше 20 символов', '.{1,15}'),
                'Цена(Фирма)': ('price_manufacturer', '1234', 4, 'text', 'required', 'Допускаются только цифры и<br>длина меньше 4 символов', '[0-9]{1,4}'),
                'Цена(Аптека)': ('price_pharmacy', '9876', 4, 'text', 'required', 'Допускаются только цифры и<br>длина меньше 4 символов', '[0-9]{1,4}'),
                'Дефект': ('defect', '1', 1, 'checkbox', '?', '.{0,100}')}
