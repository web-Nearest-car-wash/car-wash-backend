from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from carwash.models import CarWash
from api.carwash.serializers import CarWashSerializer


class CarWashViewSet(ModelViewSet):
    queryset = CarWash.objects.all()
    serializer_class = CarWashSerializer
    permission_classes = [AllowAny]
