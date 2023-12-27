from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CarWashViewSet

router = SimpleRouter()

router.register(r'carwashes', CarWashViewSet, basename='carwashes')

urlpatterns = [
    path('', include(router.urls)),
]
