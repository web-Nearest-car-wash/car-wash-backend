from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters
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
    """

    queryset = CarWashModel.objects.all().annotate(
        rating=Avg('carwashratingmodel__score'))
    serializer_class = CarWashSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CarWashFilter
    ordering_fields = ('rating',)
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_serializer_class(self):
        """Возвращает соответствующий класс сериализатора в
        зависимости от действия."""
        if self.action == 'list':
            return CarWashSerializer
        return CarWashCardSerializer
