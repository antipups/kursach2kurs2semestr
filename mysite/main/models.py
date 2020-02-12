from django.db import models


################################################################

# ____________________________ФИРМА___________________________ #

################################################################


class Country(models.Model):
    """
        Таблица с странами
    """
    title_of_country = models.CharField(max_length=3)


class Manufacturer(models.Model):
    """
        Таблица с фирмами, внешние ключи:
            Country (страны).
    """
    title_of_manufact = models.CharField(max_length=30)
    id_of_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    address_of_manufact = models.CharField(max_length=10)
    email_of_manufact = models.CharField(max_length=12)
    year_of_manufact = models.IntegerField()


################################################################

# __________________________ЛЕКАРСТВА_________________________ #

################################################################


class Shape(models.Model):
    """
        Таблица форм выпуска
    """
    title_of_shape = models.CharField(max_length=15)


class Pharma_group(models.Model):
    """
        Таблица фармакалогических групп
    """
    title_of_group = models.CharField(max_length=20)


class Medicament(models.Model):
    """
        Таблица медикаментов, внешние ключи:
            Shape (форма выпуска);
            Pharma_group (фармак. группа);
            Manufacturer (фирма).
    """
    title_of_medicament = models.CharField(max_length=20)
    id_of_shape = models.ForeignKey(Shape, models.PROTECT)
    id_of_group = models.ForeignKey(Pharma_group, models.PROTECT)
    comments = models.TextField()
    bar_code = models.ImageField(width_field=100, height_field=100)
    id_of_manufact = models.ForeignKey(Manufacturer, models.CASCADE)


################################################################

# ____________________________АПТЕКИ__________________________ #

################################################################


class District(models.Model):
    """
        Таблица районов
    """
    title_of_district = models.CharField(max_length=15)


class Pharmacy(models.Model):
    """
        Таблица аптек, внешние ключи:
            District (районы).
    """
    number_of_pharmacy = models.IntegerField()
    title_of_pharmacy = models.CharField(max_length=15, help_text="Название аптеки")
    address_of_pharmacy = models.CharField(max_length=12)
    id_of_district = models.ForeignKey(District, models.PROTECT)
    phone_of_pharmacy = models.CharField(max_length=10)


################################################################

# ____________________________ПАРТИЯ__________________________ #

################################################################


class Employee(models.Model):
    """
        Таблица работника, внешние ключи:
            Pharmacy (аптека).
    """
    id_of_pharm = models.ForeignKey(Pharmacy, models.CASCADE)
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    third_name = models.CharField(max_length=20)


class Lot(models.Model):
    """
        Таблица партий, внешние ключи:
            Employee (работник).
    """
    datefact = models.DateField()
    count = models.IntegerField()
    number_of_lot = models.IntegerField()
    datestart = models.DateField()
    datefinish = models.DateField()
    price_manufact = models.IntegerField()
    price_pharm = models.IntegerField()
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    defect = models.BooleanField()
    reason = models.TextField()
