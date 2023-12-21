from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from carwash.models import CarWashModel
from core.constants import CARWASH_API_SCHEMA_EXTENSIONS
from .filters import CarWashFilter
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

    queryset = CarWashModel.objects.all().annotate(
        rating=Avg('carwashratingmodel__score'))
    serializer_class = CarWashSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarWashFilter
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_serializer_class(self):
        """Возвращает соответствующий класс сериализатора в
        зависимости от действия."""
        if self.action == 'list':
            return CarWashSerializer
        return CarWashCardSerializer
