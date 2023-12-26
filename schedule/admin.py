from django.contrib import admin

from .models import ScheduleModel


class ScheduleInline(admin.TabularInline):
    """Класс админки расписания."""

    model = ScheduleModel
