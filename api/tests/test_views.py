import unittest
from http import HTTPStatus

from rest_framework.test import APIRequestFactory, APITestCase

from api.carwash.views import CarWashViewSet, KeywordsServicesViewSet
from carwash.models import CarWashModel, CarWashTypeModel
from services.models import KeywordsServicesModel


class TestCarWashAPIViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CarWashViewSet.as_view({'get': 'list'})
        self.detail_view = CarWashViewSet.as_view({'get': 'retrieve'})
        self.type_ = CarWashTypeModel.objects.get_or_create(
            name='Test Type')[0]
        self.carwash = CarWashModel.objects.create(
            name='Test Car Wash',
            latitude='55.152011',
            longitude='37.417211',
            legal_person=True,
            loyalty='Test Loyalty',
            over_information='Test Over Information',
            rest_room=True,
            payment='cash',
        )
        self.carwash.type.add(self.type_)
        self.carwash.save()

    def tearDown(self):
        self.carwash.delete()
        self.type_.delete()

    def test_get_carwashes_list(self):
        request = self.factory.get('/carwashes/')
        response = self.view(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_carwash_detail(self):
        request = self.factory.get(f'/carwashes/{self.carwash.id}/')
        response = self.detail_view(request, pk=self.carwash.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_carwash_type_list(self):
        request = self.factory.get('/types/')
        response = self.view(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_carwash_type_detail(self):
        request = self.factory.get(f'/types/{self.type_.id}/')
        response = self.detail_view(request, pk=self.type_.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestKeywordsServicesAPIViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = KeywordsServicesViewSet.as_view({'get': 'list'})
        self.detail_view = KeywordsServicesViewSet.as_view({'get': 'retrieve'})
        self.keyword_service = KeywordsServicesModel.objects.create(
            name='TestKeywordService',
        )
        self.keyword_service.save()

    def tearDown(self):
        self.keyword_service.delete()

    def test_get_keywords_services_list(self):
        request = self.factory.get('/keywords_services/')
        response = self.view(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_keywords_services_detail(self):
        request = self.factory.get(
            f'/keywords_services/{self.keyword_service.id}/')
        response = self.detail_view(request, pk=self.keyword_service.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()
