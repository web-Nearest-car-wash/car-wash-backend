from django.db import models
from multiselectfield import MultiSelectField

from core.constants import PAYMENT_CHOICES


class ServicesModel(models.Model):
    """Класс услуг автомойки."""

    name = models.CharField(
        db_index=True,
        verbose_name='Название услуги',
        max_length=200,
        unique=True,
        help_text='Название услуги'
    )
    description = models.TextField(verbose_name='Описание услуги')
    rest_room = models.BooleanField(
        verbose_name='Комната отдыха',
        default=False,
        help_text='Наличие комнаты отдыха'
    )
    payment = MultiSelectField(
        verbose_name='Способ оплаты',
        choices=PAYMENT_CHOICES,
        max_choices=4,
        null=True,
        blank=True,
        help_text='Выберите способ оплаты',
        max_length=30
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.name}'
