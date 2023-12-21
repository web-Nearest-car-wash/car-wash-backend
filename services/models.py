from django.db import models


class ServicesModel(models.Model):
    """Модель услуг автомойки."""

    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name='Название услуги',
    )
    description = models.TextField(verbose_name='Описание услуги')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name
