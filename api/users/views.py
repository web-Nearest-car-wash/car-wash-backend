from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.paginations import CustomPageNumberPagination
from api.users.serializers import CustomUserSerializer
from users.models import User


@extend_schema_view(
    list=extend_schema(
            summary="Получить список пользователей",
        ),
    update=extend_schema(
        summary="Изменения данных о пользователе",
    ),
    partial_update=extend_schema(
        summary="Частичное изменение данных о пользователе",
        description="""Изменения данных о пользователе.
        Поля, которые не заполнены будут оставлены без изменений.""",
    ),
    create=extend_schema(
            summary="Создать нового пользователя",
        ),
    destroy=extend_schema(
        summary="Удалить пользователя",
    ),
    retrieve=extend_schema(
        summary="Получить данные о пользователе",
    )
)
class CustomUserViewSet(UserViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
