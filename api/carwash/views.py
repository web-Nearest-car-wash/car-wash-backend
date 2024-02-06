from decimal import Decimal

from django.conf import settings
from django.db.models import Avg, F
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.carwash.utils import distance_calculation
from carwash.models import CarWashModel, CarWashRatingModel, CarWashTypeModel
from core.constants import (CARWASH_API_SCHEMA_EXTENSIONS,
                            CARWASH_RATING_API_SCHEMA_EXTENSIONS,
                            CARWASH_TYPE_API_SCHEMA_EXTENSIONS,
                            KEYWORDS_SERVICES_API_SCHEMA_EXTENSIONS)
from services.models import KeywordsServicesModel

from .filters import CarWashFilter
from .serializers import (CarWashCardSerializer, CarWashRatingSerializer,
                          CarWashSerializer, CarWashTypeSerializer,
                          KeywordsServicesSerializer)


@extend_schema_view(**CARWASH_API_SCHEMA_EXTENSIONS)
class CarWashViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет предоставляет доступ к данным автомоек.

    Разрешены GET-запросы для получения списка автомоек
    и деталей конкретной автомойки.
    Доступно для любого пользователя.
    """

    queryset = CarWashModel.objects.all().annotate(
        rating=Round(Avg('carwashratingmodel__score'), 2),
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
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        """"Добавление в queryset поля расстояния
        до геопозиции для возможности сортировки"""
        user_latitude = self.request.query_params.get('latitude')
        user_longitude = self.request.query_params.get('longitude')
        if not (user_latitude and user_longitude):
            return distance_calculation(
                self.queryset,
                Decimal(settings.DEFAULT_LATITUDE),
                Decimal(settings.DEFAULT_LONGITUDE)
            )
        return self.queryset

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
    pagination_class = LimitOffsetPagination
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
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        return self.queryset.filter(
            name__in=settings.CARWASH_TYPES.split(',')
        )


@extend_schema_view(**CARWASH_RATING_API_SCHEMA_EXTENSIONS)
class CarWashRatingViewSet(ModelViewSet):
    queryset = CarWashRatingModel.objects.all()
    serializer_class = CarWashRatingSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {'success': 'Оценка успешно добавлена!'},
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
