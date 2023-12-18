from django.contrib import admin

from carwash.models import (CarWashModel, CarWashServicesModel,
                            CarWashTypeModel, MetroStationModel,
                            NearestMetroStationModel)


@admin.register(CarWashTypeModel)
class CarWashTypeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(CarWashModel)
class CarWashModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type",]


@admin.register(CarWashServicesModel)
class CarWashServiceModelAdmin(admin.ModelAdmin):
    list_display = ["carwash", "service", "price"]


@admin.register(NearestMetroStationModel)
class NearestMetroStationModelAdmin(admin.ModelAdmin):
    list_display = ["carwash", "metro_station", "distance"]


@admin.register(MetroStationModel)
class MetroStationModelAdmin(admin.ModelAdmin):
    list_display = ["name", "latitude", "longitude"]
