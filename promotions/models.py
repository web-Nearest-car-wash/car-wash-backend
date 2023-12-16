from django.db import models


class PromotionsModel(models.Model):
    """Класс текущих акций автомойки."""

    name = models.CharField(max_length=200, verbose_name='Название акции')
    description = models.TextField(verbose_name='Описание акции')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return f'{self.name}'
