from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated

from api.paginations import CustomPageNumberPagination
from api.users.serializers import CustomUserSerializer
from users.models import User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
