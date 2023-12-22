from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from carwash.models import CarWashModel


class ContactsModel(models.Model):
    """Модель контактов автомойки."""

    carwash = models.OneToOneField(
        CarWashModel,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Мойка',
    )
    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone = PhoneNumberField(
        'Номер телефона',
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )
    website = models.URLField(
        'Сайт',
        blank=True,
        null=True,
        unique=True,
    )

    class Meta:
        ordering = ('carwash',)
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return (f'{self.carwash}, телефон: {self.phone}'
                f'адрес: {self.address}, сайт: {self.website}')
