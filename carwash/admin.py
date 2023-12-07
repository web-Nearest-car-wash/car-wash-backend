from django.contrib import admin

from carwash.models import CarWashTypeModel, CarWashModel


@admin.register(CarWashTypeModel)
class CarWashTypeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(CarWashModel)
class CarWashModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "coordinates", "type"]
