from django.db import models

from .models import CarWash


class Contacts(models.Model):
    """Класс, представляющий модель контактов автомойки."""

    carwash = models.ForeignKey(
        CarWash,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='Мойка',
    )
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)

    class Meta:
        ordering = ('carwash',)
        verbose_name = 'Контакты '

    def __str__(self):
        return (f'{self.carwash}, телефон: {self.phone}'
                f'адрес: {self.address}')
