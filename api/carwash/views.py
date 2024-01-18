from decimal import Decimal
from math import cos, radians, sin

from django.conf import settings
from django.db.models import Avg, ExpressionWrapper, F, FloatField, Func
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from drf_recaptcha.validators import ReCaptchaV2Validator
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from carwash.models import CarWashModel, CarWashRatingModel, CarWashTypeModel
from core.constants import (CARWASH_API_SCHEMA_EXTENSIONS,
                            CARWASH_TYPE_API_SCHEMA_EXTENSIONS,
                            EARTH_AVERAGE_RADIUS,
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
    pagination_class = LimitOffsetPagination
    ordering_fields = ('rating', 'distance')
    search_fields = (
        'address',
        'name',
        'service__name',
        'type__name',
    )
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
                EARTH_AVERAGE_RADIUS * Func(
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
        return self.queryset.filter(
            name__in=settings.CARWASH_TYPES.split(',')
        )


RECAPTCHA_SECRET_KEY = '6LfrdFIpAAAAAHavnL0AViY8qDmayW06DrTSPJD5'


class CarWashRatingViewSet(ModelViewSet):
    queryset = CarWashRatingModel.objects.all()
    serializer_class = CarWashRatingSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            recaptcha_response = request.data.get('captcha', None)
            if recaptcha_response:
                validator = ReCaptchaV2Validator(
                    secret_key=RECAPTCHA_SECRET_KEY
                )
                try:
                    validator(recaptcha_response, None)
                except ValidationError as e:
                    return Response(
                        {'error': str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {'success': 'Rating created successfully!'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': 'reCAPTCHA response is missing'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
