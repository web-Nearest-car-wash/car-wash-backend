from datetime import datetime
from decimal import Decimal

from django.db.models import Q
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet, NumberFilter)
from django_filters.rest_framework.filters import ModelMultipleChoiceFilter

from .constants import LAT_RANGE, LONG_RANGE
from carwash.models import CarWashModel
from schedule.models import ScheduleModel
from services.models import ServicesModel


class CarWashFilter(FilterSet):
    """Фильтрация моек по местоположению, типу и услугам"""

    is_open = BooleanFilter(
        method='filter_is_open',
        label='Статус автомойки в текущий момент: открыто/закрыто'
        )

    latitude = NumberFilter(
        method='filter_by_distance',
        label='Координаты пользователя: широта'
        )

    longitude = NumberFilter(
        method='filter_by_distance',
        label='Координаты пользователя: долгота')

    services = ModelMultipleChoiceFilter(
        queryset=ServicesModel.objects.all(),
        field_name='service__name',
        to_field_name='name',
        lookup_expr='icontains',
        label='Выберите услугу'
    )

    type = CharFilter(
        field_name='type__name',
        lookup_expr='istartswith',
        label='Выберите тип автомойки'
    )

    class Meta:
        model = CarWashModel
        fields = ['latitude', 'longitude', 'services']

    def filter_by_distance(self, queryset, name, value):
        """Фильтрация по местоположени """
        latitude = self.data.get('latitude')
        longitude = self.data.get('longitude')
        if latitude and longitude:
            return queryset.filter(
                Q(latitude__range=(Decimal(latitude) - LAT_RANGE,
                  Decimal(latitude) + LAT_RANGE)) &
                Q(longitude__range=(Decimal(longitude) - LONG_RANGE,
                  Decimal(longitude) + LONG_RANGE))
            )
        return queryset

    def filter_is_open(self, queryset, name, value):
        """Фильтрация по статусу - открыто/закрыто"""
        now = datetime.now().time()
        day_of_week = datetime.now().weekday()
        open_carwashes = ScheduleModel.objects.filter(
            Q(day_of_week=day_of_week,
              opening_time__lte=now,
              closing_time__gte=now) | Q(
                day_of_week=day_of_week,
                around_the_clock=True
            )
        ).values_list('carwash')
        if value:
            return queryset.filter(id__in=open_carwashes)
        return queryset
