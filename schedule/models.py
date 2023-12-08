from django.db import models
from django.utils.translation import gettext_lazy as _

from .models import CarWash


class Schedule(models.Model):
    """Класс, представляющий модель режима работы автомойки."""

    carwash = models.ForeignKey(
        CarWash,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Мойка',
    )
    day_of_week = models.IntegerField(verbose_name='День недели', choices=[
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (7, _('Sunday')),
    ])
    opening_time = models.TimeField(verbose_name='Время открытия',)
    closing_time = models.TimeField(verbose_name='Время закрытия',)

    class Meta:
        ordering = ('carwash',)
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return (f'{self.carwash}, режим работы: в {self.day_of_week} с '
                f'{self.opening_time} до {self.closing_time}')
