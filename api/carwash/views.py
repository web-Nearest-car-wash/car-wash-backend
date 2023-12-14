from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from carwash.models import CarWashModel
from carwash.serializers import CarWashSerializer


class CarWashViewSet(ReadOnlyModelViewSet):
    queryset = CarWash.objects.all()
    serializer_class = CarWashSerializer
    permission_classes = [AllowAny]
