from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.carwash.serializers import CarWashSerializer
from carwash.models import CarWash


class CarWashViewSet(ModelViewSet):
    queryset = CarWash.objects.all()
    serializer_class = CarWashSerializer
    permission_classes = [AllowAny]
