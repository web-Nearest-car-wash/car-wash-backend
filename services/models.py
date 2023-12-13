from django.db import models


class Servises(models.Model):
    """Класс, представляющий модель услуг автомойки."""

    name = models.CharField(
        db_index=True,
        verbose_name='Название',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return {self.name}
