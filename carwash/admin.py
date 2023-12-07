from django.contrib import admin

from carwash.models import CarWashModel, CarWashTypeModel


@admin.register(CarWashTypeModel)
class CarWashTypeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(CarWashModel)
class CarWashModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "coordinates", "type"]
