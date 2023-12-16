from django.contrib import admin

from .models import PromotionsModel


class PromotionsAdmin(admin.ModelAdmin):
    """Класс админки акций."""

    list_display = ['id', 'name', 'description']
    empty_value_display = '-пусто-'

admin.site.register(PromotionsModel, PromotionsAdmin)
