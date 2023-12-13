from django.contrib import admin

from .models import Servises


class ServisesAdmin(admin.ModelAdmin):
    """Класс услуг."""

    list_display = ('id', 'name')
    empty_value_display = '-пусто-'


admin.site.register(Servises, ServisesAdmin)
