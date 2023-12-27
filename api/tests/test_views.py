import unittest

from rest_framework.test import APIRequestFactory, APITestCase

from api.carwash.views import CarWashViewSet
from carwash.models import CarWashModel, CarWashTypeModel


class TestCarWashAPIViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CarWashViewSet.as_view({'get': 'list'})
        self.detail_view = CarWashViewSet.as_view({'get': 'retrieve'})
        type_ = CarWashTypeModel.objects.create(name='Test Car Wash Type')
        self.carwash = CarWashModel.objects.create(
            name='Test Car Wash',
            latitude='55.752011',
            longitude='37.617211',
            type=type_,
            legal_person=True,
            loyalty='Test Loyalty',
            over_information='Test Over Information',
            rest_room=True,
            payment='cash',
        )

    def tearDown(self):
        self.carwash.delete()

    def test_get_carwashes_list(self):
        request = self.factory.get('/carwashes/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_carwash_detail(self):
        request = self.factory.get(f'/carwashes/{self.carwash.id}/')
        response = self.detail_view(request, pk=self.carwash.id)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
