import unittest
from django.utils import timezone

from api.carwash.serializers import CarWashSerializer
from carwash.models import CarWashModel, CarWashTypeModel
from schedule.models import ScheduleModel


# class TestCarWashSerializer(unittest.TestCase):
#     def test_get_open_until(self):
#         # Create a mock CarWashModel object
#         car_wash_model_mock = Mock()
#         car_wash_model_mock.schedules.all.return_value = [Mock(open_until='10:00 PM')]  # Replace 'open_until' with the actual attribute name
#
#         # Create an instance of CarWashSerializer
#         serializer = CarWashSerializer()
#
#         # Call the get_open_until method and assert the result
#         result = serializer.get_open_until(car_wash_model_mock)
#         self.assertEqual(result, '10:00 PM')  # Replace '10:00 PM' with the expected result
#

class TestCarWashSerializer(unittest.TestCase):

    def setUp(self):
        self.serializer = CarWashSerializer()
        self.type_ = CarWashTypeModel.objects.create(name='Test Type')
        self.carwash = CarWashModel.objects.create(
            name='Test Car Wash',
            latitude='55.752011',
            longitude='37.617211',
            type=self.type_,
            legal_person=True,
            loyalty='Test Loyalty',
            over_information='Test Over Information',
            rest_room=True,
            payment='cash',
        )
        self.schedule = ScheduleModel.objects.create(
            carwash=self.carwash,
            day_of_week=timezone.now().weekday(),
            opening_time="10:00",
            closing_time="18:00",
            around_the_clock=False,
        )

    def tearDown(self):
        self.carwash.delete()
        self.type_.delete()
        self.schedule.delete()

    def test_fields(self):
        expected_fields = (
            'id',
            'image',
            'contacts',
            'metro',
            'name',
            'rating',
            'latitude',
            'longitude',
            'open_until',
        )
        self.assertEqual(self.serializer.Meta.fields, expected_fields)

    def test_model(self):
        serializer = CarWashSerializer()
        self.assertEqual(serializer.Meta.model, CarWashModel)

    def test_get_open_until_with_schedules(self):
        serializer = CarWashSerializer(self.carwash)
        self.assertEqual(
            serializer.data['open_until'],
            f'Работает до {self.schedule.closing_time}'
        )


if __name__ == '__main__':
    unittest.main()
