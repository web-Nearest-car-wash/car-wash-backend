import unittest

from django.utils import timezone

from api.carwash.serializers import CarWashCardSerializer, CarWashSerializer
from carwash.models import CarWashModel, CarWashImageModel, CarWashTypeModel
from contacts.models import ContactsModel
from schedule.models import ScheduleModel


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


class TestCarWashCardSerializer(TestCarWashSerializer):
    """Тесты сериалайзера карточки мойки."""

    def setUp(self):
        super().setUp()
        self.serializer = CarWashCardSerializer()
        self.contacts = ContactsModel.objects.create(
            carwash=self.carwash,
            address='Ул. Тестовая, дом, корпус',
            email='test@mail.ru',
            phone='89217553535',
            website='test_website.com',
        )
        self.image = CarWashImageModel.objects.create(
            carwash=self.carwash,
            image="https://example.com/image.jpg",
            avatar=True,
        )

    def tearDown(self):
        self.carwash.delete()
        self.type_.delete()
        self.schedule.delete()

    def test_fields(self):
        """Проверка полей сериализатора."""
        expected_fields = (
            'id',
            'image',
            'contacts',
            'legal_person',
            'loyalty',
            'metro',
            'name',
            'promotions',
            'payment',
            'rating',
            'rest_room',
            'schedule',
            'services',
            'type',
            'latitude',
            'longitude',
            'over_information',
        )
        self.assertEqual(self.serializer.Meta.fields, expected_fields)

    def test_model(self):
        """Провека модели для сериалайзера."""
        self.assertEqual(self.serializer.Meta.model, CarWashModel)


if __name__ == '__main__':
    unittest.main()
