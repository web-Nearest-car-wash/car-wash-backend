from django.contrib import admin

from .models import ServisesModel


class ServisesAdmin(admin.ModelAdmin):
    """Класс админки услуг."""

    list_display = ('id', 'name', 'description')
    empty_value_display = '-пусто-'


admin.site.register(ServisesModel, ServisesAdmin)
