from django.contrib import admin

from .models import ServicesModel


class ServiсesAdmin(admin.ModelAdmin):
    """Класс админки услуг."""

    list_display = ('id', 'name', 'description')
    empty_value_display = '-пусто-'


admin.site.register(ServicesModel, ServiсesAdmin)
