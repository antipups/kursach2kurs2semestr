# Generated by Django 3.0.3 on 2020-02-12 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200212_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacy',
            name='title_of_pharmacy',
            field=models.CharField(help_text='Название аптеки', max_length=15),
        ),
    ]
