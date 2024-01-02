from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CarWashViewSet, CarWashTypeViewSet, KeywordsServicesViewSet

router = SimpleRouter()

router.register(r'carwashes', CarWashViewSet, basename='carwashes')
router.register(
    r'keywords_services',
    KeywordsServicesViewSet,
    basename='keywords_services'
)
router.register(r'types', CarWashTypeViewSet, basename='types')

urlpatterns = [
    path('', include(router.urls)),
]
