from decimal import Decimal

from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from django_filters.rest_framework.filters import ModelMultipleChoiceFilter

from .constants import LAT_RANGE, LONG_RANGE
from carwash.models import CarWashModel
from services.models import ServicesModel


class CarWashFilter(FilterSet):
    """Фильтрация моек по местоположению, типу и услугам"""

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
        """Фильтрация по местоположению """
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
