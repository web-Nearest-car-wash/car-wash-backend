from decimal import Decimal

from django.conf import settings
from django.db.models import (Avg, DecimalField,
                              ExpressionWrapper, F,
                              FloatField, Func)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from carwash.models import CarWashModel, CarWashTypeModel
from core.constants import (CARWASH_API_SCHEMA_EXTENSIONS,
                            CARWASH_TYPE_API_SCHEMA_EXTENSIONS,
                            KEYWORDS_SERVICES_API_SCHEMA_EXTENSIONS)
from services.models import KeywordsServicesModel

from .filters import CarWashFilter
from .serializers import (CarWashCardSerializer, CarWashSerializer,
                          KeywordsServicesSerializer, CarWashTypeSerializer)


@extend_schema_view(**CARWASH_API_SCHEMA_EXTENSIONS)
class CarWashViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет предоставляет доступ к данным автомоек.

    Разрешены GET-запросы для получения списка автомоек
    и деталей конкретной автомойки.
    Доступно для любого пользователя.
    """

    queryset = CarWashModel.objects.all().annotate(
        rating=Avg('carwashratingmodel__score')
    )
    serializer_class = CarWashSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CarWashFilter
    ordering_fields = ('rating', 'dist')
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset

        user_latitude = Decimal(
            self.request.query_params.get(
                'latitude', settings.DEFAULT_LATITUDE
            )
        )
        user_longitude = Decimal(
            self.request.query_params.get(
                'longitude', settings.DEFAULT_LONGITUDE
            )
        )
        queryset = queryset.annotate(
            dist=ExpressionWrapper((
                        (F('latitude') - user_latitude)*111
                ) ** 2 + (
                        (F('longitude') - user_longitude)*89
                ) ** 2,
                    output_field=DecimalField()
                )
            )
        return queryset

    def get_serializer_class(self):
        """Возвращает соответствующий класс сериализатора в
        зависимости от действия."""
        if self.action == 'list':
            return CarWashSerializer
        return CarWashCardSerializer


@extend_schema_view(**KEYWORDS_SERVICES_API_SCHEMA_EXTENSIONS)
class KeywordsServicesViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет предоставляет доступ к ключевым словам,
    необходимым для фильтрации по услугам.
    """
    queryset = KeywordsServicesModel.objects.all()
    serializer_class = KeywordsServicesSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']


@extend_schema_view(**CARWASH_TYPE_API_SCHEMA_EXTENSIONS)
class CarWashTypeViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет предоставляет доступ к типам автомоек,
    необходимым для фильтрации по типам.
    """
    queryset = CarWashTypeModel.objects.all()
    serializer_class = CarWashTypeSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        carwash_types = [
            'самообслуживания',
            'комплексная',
            'автоматическая',
            'бесконтактная',
            'ручная'
        ]
        return self.queryset.filter(
            name__in=carwash_types
        )
