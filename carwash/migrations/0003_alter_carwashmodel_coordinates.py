# Generated by Django 4.2.8 on 2023-12-16 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0002_alter_carwashmodel_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carwashmodel',
            name='coordinates',
            field=models.CharField(blank=True, max_length=200, unique=True, validators=[django.core.validators.RegexValidator(message='Неверные координаты, должны быть вида 55.752378,37.609289', regex='^-?([0-8]?[0-9]|90)(\\.[0-9]{1,10}),([0-9]{1,2}|1[0-7][0-9]|180)(\\.[0-9]{1,10})$')], verbose_name='Координаты Ш,Д'),
        ),
    ]
