import unittest

from django.utils import timezone

from api.carwash.serializers import (CarWashCardSerializer,
                                     CarWashContactsSerializer,
                                     CarWashScheduleSerializer,
                                     CarWashSerializer)
from carwash.models import CarWashImageModel, CarWashModel, CarWashTypeModel
from contacts.models import ContactsModel
from schedule.models import ScheduleModel


class TestCarWashSerializer(unittest.TestCase):

    def setUp(self):
        self.serializer = CarWashSerializer()
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
        self.contacts.delete()
        self.image.delete()

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


class TestCarWashContactsSerializer(TestCarWashCardSerializer):
    """Тесты сериалайзера контактов мойки."""

    def setUp(self):
        super().setUp()
        self.serializer = CarWashContactsSerializer()

    def test_fields(self):
        """Проверка полей сериализатора."""
        expected_data = [
            ['address', self.contacts.address],
            ['email', self.contacts.email],
            ['phone', self.contacts.phone],
            ['website', self.contacts.website],
        ]
        serialized_data = self.serializer.to_representation(self.contacts)
        for field, data in expected_data:
            with self.subTest(field=field):
                self.assertEqual(serialized_data.get(field), data)


class TestCarWashScheduleSerializer(TestCarWashSerializer):
    """Тесты сериалайзера расписания мойки."""

    def setUp(self):
        super().setUp()
        self.serializer = CarWashScheduleSerializer()

    def test_fields(self):
        """Проверка полей сериализатора."""
        expected_fields = (
            'day_of_week',
            'opening_time',
            'closing_time',
            'around_the_clock',
            'open_until_list',
        )
        self.assertEqual(self.serializer.Meta.fields, expected_fields)


if __name__ == '__main__':
    unittest.main()
