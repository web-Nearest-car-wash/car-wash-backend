from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema_view
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

    def me(self, request, *args, **kwargs):
        pass

    def resend_activation(self, request, *args, **kwargs):
        pass

    def set_password(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        pass

    def reset_password_confirm(self, request, *args, **kwargs):
        pass

    def set_username(self, request, *args, **kwargs):
        pass

    def reset_username(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass
