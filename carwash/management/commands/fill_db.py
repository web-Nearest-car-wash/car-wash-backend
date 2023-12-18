import json
import os

from django.core.management import BaseCommand

from carwash.models import CarWashModel, CarWashTypeModel
from users.models import User

JSON_PATH = os.path.join(
    os.path.dirname(__file__),
)


class Command(BaseCommand):
    help = 'Заполнение базы данных'

    def load_from_json(self, json_path, file_name):
        """
        Загрузка файла с словарь
        """
        with open(
                os.path.join(
                    json_path,
                    file_name + '.json'),
                'r',
                encoding='utf-8') as infile:
            new_list = json.loads(infile.read())
            return new_list

    def handle(self, *args, **kwargs):
        self.stdout.write('Старт заполнения базы автомоек')
        try:
            super_user = User.objects.create_superuser(
                username='admin',
                email='admin@ya.ru',
                password='admin',
                phone='+79999999999'
            )
            self.stdout.write(f'Суперюзер создан')
        except:
            self.stdout.write(f'Данный суперюзер уже существует')

        car_wash_all = self.load_from_json(JSON_PATH, 'carwash')

        self.stdout.write(f'{car_wash_all}')

        for car_wash in car_wash_all:

            print()
            self.stdout.write(f'CARRRRRRR {car_wash}')

            type_wash = CarWashTypeModel.objects.get_or_create(
                name=car_wash['type'])

            car_wash['type'] = type_wash[0]

            try:
                self.stdout.write(f'START SAVE {car_wash}')
                new_car_wash = CarWashModel.objects.create(**car_wash)
                self.stdout.write(f'SAVED CAR_WASH {new_car_wash}')
            except:
                self.stdout.write(f'ERROR CAR_WASH ALREADY EXIST {car_wash}')
