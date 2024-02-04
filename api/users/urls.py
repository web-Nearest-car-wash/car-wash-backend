from django.urls import include, path
from rest_framework import routers

from api.users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register('auth/users', CustomUserViewSet, basename='users')


def is_route_selected(url_pattern):
    urls = [
        'auth/users/activation/',
    ]

    for u in urls:
        match = url_pattern.resolve(u)
        if match:
            return False
    return True


selected_user_routes = list(filter(is_route_selected, router.urls))

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),

] + selected_user_routes
