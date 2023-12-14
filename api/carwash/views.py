from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from carwash.models import CarWashModel
from core.constants import CARWASH_API_SCHEMA_EXTENSIONS
from .serializers import CarWashSerializer, CarWashCardSerializer


@extend_schema_view(**CARWASH_API_SCHEMA_EXTENSIONS)
class CarWashViewSet(ReadOnlyModelViewSet):
    queryset = CarWashModel.objects.all()
    serializer_class = CarWashSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return CarWashSerializer
        return CarWashCardSerializer
