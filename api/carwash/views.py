from decimal import Decimal

from django.db.models import Avg, F
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from geopy.distance import geodesic
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from carwash.models import CarWashModel
from core.constants import (CARWASH_API_SCHEMA_EXTENSIONS,
                            CENTER_MOSCOW_LATITUDE, CENTER_MOSCOW_LONGITUDE)

from .filters import CarWashFilter
from .serializers import CarWashCardSerializer, CarWashSerializer


@extend_schema_view(**CARWASH_API_SCHEMA_EXTENSIONS)
class CarWashViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет предоставляет доступ к данным автомоек.

    Разрешены GET-запросы для получения списка автомоек
    и деталей конкретной автомойки.
    Доступно для любого пользователя.
    """

    queryset = CarWashModel.objects.all().annotate(
        rating=Avg('carwashratingmodel__score'))
    serializer_class = CarWashSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CarWashFilter
    ordering_fields = ('rating', 'distance')
    permission_classes = [AllowAny]
    http_method_names = ['get',]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        if not latitude or not longitude:
            location = (CENTER_MOSCOW_LATITUDE, CENTER_MOSCOW_LONGITUDE)
        else:
            location = (Decimal(latitude), Decimal(longitude))
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            distance=geodesic(('latitude', 'longitude'), location)
        )
        return queryset

    def get_serializer_class(self):
        """Возвращает соответствующий класс сериализатора в
        зависимости от действия."""
        if self.action == 'list':
            return CarWashSerializer
        return CarWashCardSerializer
