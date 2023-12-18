from django.db import models


class ServicesModel(models.Model):
    """Класс услуг автомойки."""

    name = models.CharField(
        db_index=True,
        verbose_name='Название услуги',
    )
    description = models.TextField(verbose_name='Описание услуги')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return {self.name}
