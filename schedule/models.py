from django.core.exceptions import ValidationError
from django.db import models

from carwash.models import CarWashModel
from core.constants import AROUND_THE_CLOCK, DAYS_OF_WEEK, SCHEDULE_HELP_TEXT


class ScheduleModel(models.Model):
    """Класс режима работы автомойки."""

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
        help_text=SCHEDULE_HELP_TEXT,
    )
    closing_time = models.TimeField(
        verbose_name='Время закрытия',
        blank=True,
        null=True,
        help_text=SCHEDULE_HELP_TEXT,
    )
    around_the_clock = models.BooleanField(
        verbose_name='Круглосуточно',
        default=False,
    )

    class Meta:
        ordering = ('carwash',)
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def get_day_of_week(self):
        if self.day_of_week is not None:
            return DAYS_OF_WEEK[self.day_of_week][1]
        return None

    def __str__(self):
        if self.around_the_clock:
            return AROUND_THE_CLOCK
        return (
            f'{self.carwash}, режим работы в "{self.get_day_of_week()}" с '
            f'{self.opening_time} до {self.closing_time}'
        )

    def clean(self):
        super().clean()
        if ScheduleModel.objects.filter(
            carwash=self.carwash,
            day_of_week=self.day_of_week
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Режим работы для "{self.get_day_of_week()}" уже задан.'
            )
        if self.opening_time is not None and self.closing_time is not None:
            if self.opening_time >= self.closing_time:
                raise ValidationError(
                    'Время начала должно быть раньше времени конца работы.')
