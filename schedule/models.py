from django.core.exceptions import ValidationError
from django.db import models

from carwash.models import CarWashModel
from core.constants import DAYS_OF_WEEK


class ScheduleModel(models.Model):
    """Модель режима работы автомойки."""

    carwash = models.ForeignKey(
        CarWashModel,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Мойка',
    )
    day_of_week = models.IntegerField(
        verbose_name='День недели',
        choices=DAYS_OF_WEEK,
        blank=True,
        null=True,
    )
    opening_time = models.TimeField(
        verbose_name='Время открытия',
        blank=True,
        null=True,
    )
    closing_time = models.TimeField(
        verbose_name='Время закрытия',
        blank=True,
        null=True,
    )
    around_the_clock = models.BooleanField(
        verbose_name='Круглосуточно',
        default=False,
    )

    class Meta:
        ordering = ('carwash',)
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        if self.around_the_clock:
            return 'Круглосуточно'
        return (f'{self.carwash}, режим работы: в {self.day_of_week} с '
                f'{self.opening_time} до {self.closing_time}')

    def clean(self):
        super().clean()
        if ScheduleModel.objects.filter(
            carwash=self.carwash,
            day_of_week=self.day_of_week
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Режим работы для "{DAYS_OF_WEEK[self.day_of_week][1]}" '
                'уже задан.'
            )
        if self.opening_time >= self.closing_time:
            raise ValidationError(
                'Время начала должно быть раньше времени конца работы.')
