# Generated by Django 3.0.3 on 2020-02-24 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200219_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='address_of_manufacturer',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='title_of_pharmacy',
            field=models.CharField(max_length=15),
        ),
    ]
