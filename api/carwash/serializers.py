import datetime as dt
from math import atan2, cos, radians, sin, sqrt

from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carwash.models import (CarWashImageModel, CarWashModel,
                            CarWashServicesModel, CarWashTypeModel,
                            MetroStationModel)
from contacts.models import ContactsModel
from core.constants import (AROUND_THE_CLOCK, CLOSED, NO_INFORMATION,
                            PAYMENT_CHOICES, TIME_UTC_CORRECTION, WORKS_UNTIL)
from promotions.models import PromotionsModel
from schedule.models import ScheduleModel


class CarWashTypeSerializer(ModelSerializer):
    """Сериализатор для типа мойки."""

    class Meta:
        fields = ('name',)
        model = CarWashTypeModel


class CarWashServicesSerializer(ModelSerializer):
    """
    Сериализатор для услуг мойки
    """
    name = serializers.ReadOnlyField(
        source='service.name', read_only=True
    )
    description = serializers.ReadOnlyField(
        source='service.description', read_only=True
    )

    class Meta:
        fields = ('name', 'description', 'price')
        model = CarWashServicesModel


class CarWashContactsSerializer(ModelSerializer):
    """
    Сериализатор для контактов мойки
    """

    class Meta:
        fields = ('address', 'phone', 'website')
        model = ContactsModel


class CarWashMetroSerializer(ModelSerializer):
    """
    Сериализатор для метро мойки
    """
    name = serializers.CharField(source='metro_station.name')

    class Meta:
        fields = ('name',)
        model = MetroStationModel


class CarWashScheduleSerializer(ModelSerializer):
    """
    Сериализатор для расписания мойки
    """
    day_of_week = serializers.SerializerMethodField()
    open_until_list = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'day_of_week',
            'opening_time',
            'closing_time',
            'around_the_clock',
            'open_until_list',
        )
        model = ScheduleModel

    @staticmethod
    def get_day_of_week(obj):
        return [schedule.get_day_of_week() for schedule in obj]

    @staticmethod
    def get_open_until_list(obj):
        current_day_of_week = dt.date.today().weekday()
        current_time = dt.datetime.now() + TIME_UTC_CORRECTION
        today_schedule = obj.filter(
            Q(day_of_week=current_day_of_week) | Q(around_the_clock=True)
        ).first()
        if today_schedule:
            if today_schedule.around_the_clock:
                return AROUND_THE_CLOCK
            if today_schedule.opening_time and today_schedule.closing_time:
                if current_time.time() < today_schedule.closing_time:
                    return (f'{WORKS_UNTIL}'
                            f'{today_schedule.closing_time.strftime("%H:%M")}')
            return CLOSED
        return NO_INFORMATION


class CarWashPromotionsSerializer(ModelSerializer):
    """
    Сериализатор для акций мойки
    """

    class Meta:
        fields = ('name', 'description')
        model = PromotionsModel


class CarWashImageSerializer(ModelSerializer):
    """
    Сериализатор для фотографий мойки
    """

    class Meta:
        fields = ('image', 'avatar')
        model = CarWashImageModel


class CarWashCardSerializer(ModelSerializer):
    """
    Сериализатор GET для карточки мойки
    """
    type = CarWashTypeSerializer()
    rating = serializers.FloatField(read_only=True)
    services = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    metro = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    promotions = CarWashPromotionsSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    rest_room = serializers.BooleanField()
    payment = serializers.MultipleChoiceField(
        read_only=True, choices=PAYMENT_CHOICES
    )

    class Meta:
        fields = (
            'id',
            'image',
            'contacts',
            'legal_person',
            'loyalty',
            'metro',
            'name',
            'promotions',
            'payment',
            'rating',
            'rest_room',
            'schedule',
            'services',
            'type',
            'latitude',
            'longitude',
            'over_information',
        )
        model = CarWashModel

    def get_metro(self, obj):
        car_wash_longitude = obj.longitude
        car_wash_latitude = obj.latitude

        all_metro_stations = MetroStationModel.objects.all()

        nearest_metro_station = None

        min_distance = float('inf')

        for metro_station in all_metro_stations:
            metro_station_longitude = metro_station.longitude
            metro_station_latitude = metro_station.latitude

            lat1, lon1, lat2, lon2 = map(
                float,
                [
                    car_wash_latitude,
                    car_wash_longitude,
                    metro_station_latitude,
                    metro_station_longitude
                ]
            )
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371 * c
            if distance < min_distance:
                min_distance = distance
                nearest_metro_station = metro_station
        if not nearest_metro_station:
            return None
        return {
            'name': nearest_metro_station.name,
            'latitude': nearest_metro_station.latitude,
            'longitude': nearest_metro_station.longitude
        }

    @staticmethod
    def get_image(obj):
        queryset = obj.carwashimagemodel_set.all()
        return CarWashImageSerializer(queryset, many=True).data

    @staticmethod
    def get_services(obj):
        queryset = obj.carwashservicesmodel_set.all()
        return CarWashServicesSerializer(queryset, many=True).data

    @staticmethod
    def get_contacts(obj):
        queryset = ContactsModel.objects.filter(
            carwash=obj
        ).first()
        return CarWashContactsSerializer(queryset).data

    @staticmethod
    def get_schedule(obj):
        queryset = obj.schedules.all()
        if queryset:
            return CarWashScheduleSerializer(queryset).data
        return None


class CarWashSerializer(CarWashCardSerializer):
    """Сериализатор для вывода моек на главной странице."""

    open_until = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'image',
            'contacts',
            'metro',
            'name',
            'rating',
            'latitude',
            'longitude',
            'open_until',
        )
        model = CarWashModel

    @staticmethod
    def get_open_until(obj):
        queryset = obj.schedules.all()
        if queryset:
            serializer = CarWashScheduleSerializer(queryset)
            return serializer.get_open_until_list(queryset)
        return None
