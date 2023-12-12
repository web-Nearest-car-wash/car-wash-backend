from django.contrib import admin

from .models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    """Класс расписания."""

    list_display = ('id', 'carwash', 'day_of_week', 'opening_time',
                    'closing_time')
    empty_value_display = '-пусто-'


admin.site.register(Schedule, ScheduleAdmin)
