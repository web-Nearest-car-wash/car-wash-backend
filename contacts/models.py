from django.db import models

from carwash.models import CarWashModel


class ContactsModel(models.Model):
    """Класс контактов автомойки."""

    carwash = models.OneToOneField(
        CarWashModel,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Мойка',
    )
    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField(max_length=15, verbose_name='Телефон')

    class Meta:
        ordering = ('carwash',)
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return (f'{self.carwash}, телефон: {self.phone}'
                f'адрес: {self.address}')
