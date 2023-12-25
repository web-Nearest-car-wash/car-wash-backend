# Generated by Django 4.2.8 on 2023-12-19 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carwash', '0006_alter_carwashservicesmodel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarWashRatingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('carwash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='carwash.carwashmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='carwashratingmodel',
            constraint=models.UniqueConstraint(fields=('carwash', 'user'), name='unique_carwash_user'),
        ),
    ]
