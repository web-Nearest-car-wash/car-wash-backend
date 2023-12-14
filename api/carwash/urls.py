from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CarWashViewSet

app_name = 'api'

v1_router = SimpleRouter()

v1_router.register(r'carwashes', CarWashViewSet, basename='carwashes')

urlpatterns = [
    path('', include(v1_router.urls)),
]
