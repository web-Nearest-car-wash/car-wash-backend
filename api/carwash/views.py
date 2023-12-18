from decimal import Decimal

from django.db.models import Q
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from carwash.models import CarWashModel
from core.constants import CARWASH_API_SCHEMA_EXTENSIONS
from .constants import LAT_RANGE, LONG_RANGE
from .serializers import CarWashSerializer, CarWashCardSerializer


@extend_schema_view(**CARWASH_API_SCHEMA_EXTENSIONS)
class CarWashViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет предоставляет доступ к данным автомоек.

    Разрешены GET-запросы для получения списка автомоек
    и деталей конкретной автомойки.
    Доступно для любого пользователя.

    Эндпоинты:
    - /carwashes/ : GET-запрос возвращает список всех автомоек.
    - /carwashes/{id}/ : GET-запрос возвращает детали автомойки по ее id.

    Если в GET-запросе передана геопозиция пользователя (latitude, longitude):
    - /carwashes/?latitude={latitude}&longitude={longitude} :
    возвращает список автомоек в заданной области,
    определяемой параметрами LAT_RANGE и LONG_RANGE,
    в зависимости от геопозиции.
    """

    queryset = CarWashModel.objects.all()
    serializer_class = CarWashSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def list(self, request):
        """Выводит список моек в заданной области.
        Если геопозиция пользователя не передана,
        выводит все мойки."""
        latitude_str = request.query_params.get('latitude')
        longitude_str = request.query_params.get('longitude')

        if latitude_str and longitude_str:
            latitude = Decimal(latitude_str)
            longitude = Decimal(longitude_str)

            nearby_carwashes = self.queryset.filter(
                Q(latitude__range=(latitude - LAT_RANGE,
                  latitude + LAT_RANGE)) &
                Q(longitude__range=(longitude - LONG_RANGE,
                  longitude + LONG_RANGE))
            )
        else:
            nearby_carwashes = self.queryset

        serializer = CarWashSerializer(nearby_carwashes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        """Возвращает соответствующий класс сериализатора в
        зависимости от действия."""
        if self.action == 'list':
            return CarWashSerializer
        return CarWashCardSerializer
