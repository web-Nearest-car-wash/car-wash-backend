from django.db import models


class ServicesModel(models.Model):
    """Класс услуг автомойки."""

    name = models.CharField(
        db_index=True,
        verbose_name='Название услуги',
        max_length=200,
        unique=True,
        help_text='Название услуги'
    )
    description = models.TextField(verbose_name='Описание услуги',
                                   blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.name}'


class KeywordsServicesModel(models.Model):
    """Класс ключевых слов для услуг автомоек."""

    name = models.CharField(
        db_index=True,
        verbose_name='Ключевое слово',
        max_length=100,
        unique=True,
        help_text='Ключевое слово'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ключевое слово услуги'
        verbose_name_plural = 'Ключевые слова услуг'

    def __str__(self):
        return f'{self.name}'
