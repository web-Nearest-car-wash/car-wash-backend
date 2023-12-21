from decimal import Decimal

from django.db.models import Q
from django_filters.rest_framework import FilterSet, NumberFilter

from .constants import LAT_RANGE, LONG_RANGE
from carwash.models import CarWashModel


class CarWashFilter(FilterSet):
    latitude = NumberFilter(method='filter_by_distance')
    longitude = NumberFilter(method='filter_by_distance')

    class Meta:
        model = CarWashModel
        fields = ['latitude', 'longitude']

    def filter_by_distance(self, queryset, name, value):
        latitude = self.data.get('latitude')
        longitude = self.data.get('longitude')
        if latitude and longitude:
            nearby_carwashes = queryset.filter(
                Q(latitude__range=(Decimal(latitude) - LAT_RANGE,
                  Decimal(latitude) + LAT_RANGE)) &
                Q(longitude__range=(Decimal(longitude) - LONG_RANGE,
                  Decimal(longitude) + LONG_RANGE))
            )
            return nearby_carwashes
        return queryset
