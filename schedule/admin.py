from django.contrib import admin

from .models import ScheduleModel


class ScheduleAdmin(admin.ModelAdmin):
    """Класс админки расписания."""

    list_display = ('id', 'carwash', 'day_of_week', 'opening_time',
                    'closing_time', 'around_the_clock')
    empty_value_display = '-пусто-'


admin.site.register(ScheduleModel, ScheduleAdmin)
