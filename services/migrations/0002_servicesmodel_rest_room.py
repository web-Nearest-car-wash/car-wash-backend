# Generated by Django 4.2.8 on 2023-12-21 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesmodel',
            name='rest_room',
            field=models.BooleanField(default=False, verbose_name='Комната отдыха'),
        ),
    ]
