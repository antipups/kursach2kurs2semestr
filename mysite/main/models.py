from django.db import models


################################################################

# ____________________________ФИРМА___________________________ #

################################################################


class Country(models.Model):
    """
        Таблица с странами
    """
    title_of_country = models.CharField(max_length=3)

    @staticmethod
    def readable():
        return 'id', 'title_of_country'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_country


class Manufacturer(models.Model):
    """
        Таблица с фирмами, внешние ключи:
            Country (страны).
    """
    title_of_manufacturer = models.CharField(max_length=30)
    id_of_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    address_of_manufacturer = models.CharField(max_length=10)
    email_of_manufacturer = models.CharField(max_length=12)
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

################################################################

# __________________________ЛЕКАРСТВА_________________________ #

################################################################


class Shape(models.Model):
    """
        Таблица форм выпуска
    """
    title_of_shape = models.CharField(max_length=15)

    @staticmethod
    def readable():
        return 'id', 'title_of_shape'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_shape


class Pharma_group(models.Model):
    """
        Таблица фармакалогических групп
    """
    title_of_pharma_group = models.CharField(max_length=20)

    @staticmethod
    def readable():
        return 'id', 'title_of_pharma_group'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_pharma_group


class Medicament(models.Model):
    """
        Таблица медикаментов, внешние ключи:
            Shape (форма выпуска);
            Pharma_group (фармак. группа);
            Manufacturer (фирма).
    """
    title_of_medicament = models.CharField(max_length=20)
    id_of_shape = models.ForeignKey(Shape, models.PROTECT)
    id_of_pharma_group = models.ForeignKey(Pharma_group, models.PROTECT)
    comments = models.TextField()
    bar_code = models.ImageField()
    id_of_manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)

    @staticmethod
    def readable():
        return 'id', 'title_of_medicament', 'id_of_shape', 'id_of_pharma_group',\
               'comments', 'bar_code', 'id_of_manufacturer'

    @staticmethod
    def readable_rus():
        return 'id', 'Название', 'Форма выпуска', 'Фармакологическая группа',\
               'Инструкция', 'Штрих-код', 'Фирма'

    def getter(self):
        return self.id, self.title_of_medicament, self.id_of_shape.title_of_shape, self.id_of_pharma_group.title_of_pharma_group, self.comments, self.bar_code, self.id_of_manufacturer.title_of_manufacturer

################################################################

# ____________________________АПТЕКИ__________________________ #

################################################################


class District(models.Model):
    """
        Таблица районов
    """
    title_of_district = models.CharField(max_length=15)

    @staticmethod
    def readable():
        return 'id', 'title_of_district'

    @staticmethod
    def readable_rus():
        return 'id', 'Название'

    def getter(self):
        return self.id, self.title_of_district


class Pharmacy(models.Model):
    """
        Таблица аптек, внешние ключи:
            District (районы).
    """

    number_of_pharmacy = models.IntegerField()
    title_of_pharmacy = models.CharField(max_length=15)
    address_of_pharmacy = models.CharField(max_length=12)
    id_of_district = models.ForeignKey(District, models.PROTECT)
    phone_of_pharmacy = models.CharField(max_length=10)

    @staticmethod
    def readable():
        return 'id', 'number_of_pharmacy', 'title_of_pharmacy', \
               'address_of_pharmacy', 'id_of_district', 'phone_of_pharmacy'

    @staticmethod
    def readable_rus():
        return 'id', 'Номер', 'Название', 'Адрес', 'Район', 'Телефон'

    def getter(self):
        return self.id, self.number_of_pharmacy, self.title_of_pharmacy, self.address_of_pharmacy, self.id_of_district.title_of_district, self.phone_of_pharmacy


################################################################

# ____________________________ПАРТИЯ__________________________ #

################################################################


class Employee(models.Model):
    """
        Таблица работника, внешние ключи:
            Pharmacy (аптека).
    """
    id_of_pharmacy = models.ForeignKey(Pharmacy, models.CASCADE)
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


class Lot(models.Model):
    """
        Таблица партий, внешние ключи:
            Employee (работник).
            Medicament (лекарство)
    """
    id_of_medicament = models.ForeignKey(Medicament, models.DO_NOTHING)
    datefact = models.DateField()
    count = models.IntegerField()
    number_of_lot = models.IntegerField()
    datestart = models.DateField()
    datefinish = models.DateField()
    price_manufacturer = models.IntegerField()
    price_pharmacy = models.IntegerField()
    id_of_employee = models.ForeignKey(Employee, models.DO_NOTHING)
    defect = models.BooleanField()
    reason = models.TextField()

    @staticmethod
    def readable():
        return 'id', 'id_of_medicament', 'datefact', 'count', 'number_of_lot', 'datestart', 'datefinish', \
               'price_manufacturer', 'price_pharmacy', 'id_of_employee', 'defect', 'reason'

    @staticmethod
    def readable_rus():
        return 'id', 'Лекарство', 'Дата доставки', 'Кол-во упаковок', 'Номер', 'Дата выпуска', 'Дата срока годности', \
               'Цена(Фирма)', 'Цена(Аптека)', 'Работник', 'Дефект', 'Причина возврата'

    def getter(self):
        return self.id, self.id_of_medicament.title_of_medicament, self.datefact, self.count, self.number_of_lot, self.datestart, self.datefinish, \
               self.price_manufacturer, self.price_pharmacy, \
               ' '.join((self.id_of_employee.second_name, self.id_of_employee.first_name[0] + '. ', self.id_of_employee.third_name[0] + '.')), \
               self.defect, self.reason
