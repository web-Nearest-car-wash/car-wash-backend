# Generated by Django 4.2.8 on 2023-12-21 06:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0010_alter_carwashratingmodel_carwash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carwashmodel',
            name='latitude',
            field=models.DecimalField(decimal_places=9, default='55.7520233', max_digits=11, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='carwashmodel',
            name='longitude',
            field=models.DecimalField(decimal_places=9, default='37.6174994', max_digits=12, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='metrostationmodel',
            name='latitude',
            field=models.DecimalField(decimal_places=9, max_digits=11, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='metrostationmodel',
            name='longitude',
            field=models.DecimalField(decimal_places=9, max_digits=12, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Долгота'),
        ),
    ]