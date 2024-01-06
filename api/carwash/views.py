from decimal import Decimal
from math import sin, cos, radians

from django.conf import settings
from django.db.models import (Avg, FloatField,
                              ExpressionWrapper, F, Func)
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
        rating=Avg('carwashratingmodel__score'),
        address=F('contactsmodel__address')
    )
    serializer_class = CarWashSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    )
    filterset_class = CarWashFilter
    ordering_fields = ('rating', 'distance')
    search_fields = (
        'address',
        'name',
        'service__name',
        'type__name',
    )
    ordering_fields = ('rating',)
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        """"Добавление в queryset поля расстояния
        до геопозиции для возможности сортировки"""
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
        return self.queryset.annotate(
            distance=ExpressionWrapper(
                6371 * Func(
                    Func(
                        Func(F('latitude'), function='RADIANS'),
                        function='SIN'
                    )*sin(
                        radians(user_latitude)
                    ) + Func(
                        Func(F('latitude'), function='RADIANS'),
                        function='COS'
                    )*cos(radians(user_latitude))*Func(
                        Func(
                            F('longitude'), function='RADIANS'
                        )-radians(user_longitude),
                        function='COS'
                    ), function='ACOS'
                ),
                output_field=FloatField()
            ),
        )

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
