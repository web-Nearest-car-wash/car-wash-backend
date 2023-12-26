from django.contrib import admin

from carwash.models import (CarWashImageModel, CarWashModel,
                            CarWashRatingModel, CarWashServicesModel,
                            CarWashTypeModel, MetroStationModel,
                            NearestMetroStationModel)
from contacts.admin import ContactsAdmin
from schedule.admin import ScheduleInline


@admin.register(CarWashTypeModel)
class CarWashTypeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CarWashModel)
class CarWashModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'latitude', 'longitude', 'type', ]
    inlines = [ContactsAdmin, ScheduleInline]


@admin.register(CarWashServicesModel)
class CarWashServiceModelAdmin(admin.ModelAdmin):
    list_display = ['carwash', 'service', 'price']


@admin.register(NearestMetroStationModel)
class NearestMetroStationModelAdmin(admin.ModelAdmin):
    list_display = ['carwash', 'metro_station', 'distance']


@admin.register(MetroStationModel)
class MetroStationModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']


@admin.register(CarWashRatingModel)
class CarWashRatingModelAdmin(admin.ModelAdmin):
    list_display = ['carwash', 'score', 'user', 'pub_date']


@admin.register(CarWashImageModel)
class CarWashImageModelAdmin(admin.ModelAdmin):
    list_display = ['carwash', 'image', 'avatar']
