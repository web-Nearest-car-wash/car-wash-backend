from django.contrib import admin

from .models import KeywordsServicesModel, ServicesModel


class ServicesAdmin(admin.ModelAdmin):
    """Класс админки услуг."""

    list_display = ('id', 'name', 'description')
    empty_value_display = '-пусто-'


admin.site.register(ServicesModel, ServicesAdmin)


@admin.register(KeywordsServicesModel)
class KeywordsServicesModelAdmin(admin.ModelAdmin):
    list_display = ['name']
