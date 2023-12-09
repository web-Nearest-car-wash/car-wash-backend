from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from api.paginations import CustomPageNumberPagination
from api.users.serializers import CustomUserSerializer
from core.constants import USERS_API_SCHEMA_EXTENSIONS
from users.models import User


@extend_schema_view(**USERS_API_SCHEMA_EXTENSIONS)
class CustomUserViewSet(UserViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
