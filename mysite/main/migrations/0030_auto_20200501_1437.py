# Generated by Django 3.0.3 on 2020-05-01 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20200428_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='id_of_medicament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Medicament'),
        ),
    ]
