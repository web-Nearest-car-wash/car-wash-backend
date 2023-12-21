from django.db import models

from carwash.models import CarWashModel


class PromotionsModel(models.Model):
    """Класс текущих акций автомойки."""

    name = models.CharField(max_length=200, verbose_name='Название акции')
    description = models.TextField(verbose_name='Описание акции')
    carwash = models.ForeignKey(
        CarWashModel,
        verbose_name='Автомойка',
        on_delete=models.CASCADE,
        related_name='promotions',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return f'{self.name}'
