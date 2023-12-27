from django.urls import include, path
from rest_framework import routers

from api.users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register('auth/users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
