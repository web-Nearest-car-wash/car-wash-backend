import datetime as dt

from django.db.models import Q
from drf_recaptcha.fields import ReCaptchaV2Field
from geopy.distance import geodesic
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carwash.models import (CarWashImageModel, CarWashModel,
                            CarWashRatingModel, CarWashServicesModel,
                            CarWashTypeModel, MetroStationModel)
from contacts.models import ContactsModel
from core.constants import (AROUND_THE_CLOCK, CLOSED, NO_INFORMATION,
                            PAYMENT_CHOICES, TIME_UTC_CORRECTION, WORKS_UNTIL)
from promotions.models import PromotionsModel
from schedule.models import ScheduleModel
from services.models import KeywordsServicesModel


class CarWashTypeSerializer(ModelSerializer):
    """Сериализатор для типа мойки."""

    class Meta:
        fields = ('name',)
        model = CarWashTypeModel


class KeywordsServicesSerializer(ModelSerializer):
    """Сериализатор для ключевых слов в услугах."""

    name = serializers.CharField(max_length=50)

    class Meta:
        fields = ('name',)
        model = KeywordsServicesModel


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
        fields = ('address', 'email', 'phone', 'website')
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
                if today_schedule.opening_time == today_schedule.closing_time:
                    return AROUND_THE_CLOCK
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
    type = CarWashTypeSerializer(many=True, read_only=True)
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
        carwash_longitude = obj.longitude
        carwash_latitude = obj.latitude
        carwash_coordinates = (carwash_latitude, carwash_longitude)

        all_metro_stations = MetroStationModel.objects.all()

        nearest_metro_station = None

        min_distance = float('inf')

        for metro_station in all_metro_stations:
            metro_station_longitude = metro_station.longitude
            metro_station_latitude = metro_station.latitude
            metro_station_coordinates = (
                metro_station_latitude, metro_station_longitude
            )

            distance = geodesic(
                carwash_coordinates, metro_station_coordinates
            ).km
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

    # services = serializers.SerializerMethodField()
    distance = serializers.FloatField()
    open_until = serializers.SerializerMethodField()
    # type = CarWashTypeSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'image',
            'contacts',
            'metro',
            'name',
            'rating',
            # 'services',
            # 'type',
            'latitude',
            'longitude',
            'distance',
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

    # @staticmethod
    # def get_services(obj):
    #     queryset = obj.carwashservicesmodel_set.all()
    #     return CarWashServicesSerializer(queryset, many=True).data


class CarWashRatingSerializer(serializers.ModelSerializer):
    captcha = ReCaptchaV2Field()
    carwash_id = serializers.IntegerField()

    class Meta:
        model = CarWashRatingModel
        fields = ['score', 'carwash_id', 'captcha']

    def validate_carwash_id(self, value):
        if not CarWashModel.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Мойки с указанным ID не существует."
            )
        return value

    def create(self, validated_data):
        carwash_id = validated_data.pop('carwash_id')
        carwash = CarWashModel.objects.get(id=carwash_id)
        return CarWashRatingModel.objects.create(
            carwash=carwash, **validated_data
        )
