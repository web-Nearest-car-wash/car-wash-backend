import json
from datetime import datetime

from django.core.management import BaseCommand

from carwash.models import (CarWashModel, CarWashServicesModel,
                            CarWashTypeModel, MetroStationModel)
from contacts.models import ContactsModel
from schedule.models import ScheduleModel
from services.models import ServicesModel

payment_metods = {
    "cash": ["наличными", ],
    "card": ["оплата картой", "безналичная", "оплата кредитной картой", ],
    "online": ["банковским переводом", "онлайн", "электронными деньгами", ],
    "SBP": ["СБП", "QR-код", "sms-платеж"]
}


class Command(BaseCommand):
    help = "Loads data from json"

    def handle(self, *args, **options):

        with open("data/data_output.json", encoding='utf-8') as f:
            json_data = json.load(f)
        metro_data = json_data.get("metro")
        for metro in metro_data:
            try:
                if not MetroStationModel.objects.filter(
                        name=metro["name"]
                ).exists():
                    metro = MetroStationModel(**metro)
                    metro.save()
            except Exception:
                continue
        carwashes_data = json_data.get("car_washes")
        print("carwashes_data")
        for carwash_data in carwashes_data:
            try:
                carwash, _ = CarWashModel.objects.get_or_create(
                    name=carwash_data["name"][0],
                    latitude=carwash_data["latitude"][0],
                    longitude=carwash_data["longitude"][0]
                )
            except Exception as err:
                print(f'{err} carwash_data')
                continue
            try:
                for type in carwash_data["car_wash_type"]:
                    carwash.type.add(CarWashTypeModel.objects.get_or_create(
                        name=type["name"])[0]
                                     )
                    carwash.save()
            except Exception as err:
                print(f'{err} type')
                pass
            try:
                list_of_payments = []
                for pay in carwash_data["payment_method"]:
                    if pay["name"] in payment_metods["cash"]:
                        if "cash" not in list_of_payments:
                            list_of_payments.append("cash")
                    elif pay["name"] in payment_metods["card"]:
                        if "card" not in list_of_payments:
                            list_of_payments.append("card")
                    elif pay["name"] in payment_metods["online"]:
                        if "online" not in list_of_payments:
                            list_of_payments.append("online")
                    elif pay["name"] in payment_metods["SBP"]:
                        if "SBP" not in list_of_payments:
                            list_of_payments.append("SBP")
                carwash.payment = list_of_payments
                carwash.save()
            except Exception as err:
                print(f'{err} payment')
                pass
            try:
                contact = ContactsModel(
                    carwash=carwash,
                    address=carwash_data.get("address"),
                    phone=carwash_data.get("phone"),
                    website=carwash_data.get("site")
                )
                contact.save()
            except Exception as err:
                print(f'{err} contact')
                pass
            try:
                for day_work_time in carwash_data.get("working_time"):

                    work_time = ScheduleModel(
                        carwash=carwash,
                        day_of_week=day_work_time["day_of_week"],
                        opening_time=datetime.strptime(
                            day_work_time["opening_time"], "%H:%M"
                        ).time(),
                        closing_time=datetime.strptime(
                            day_work_time["closing_time"], "%H:%M"
                        ).time()
                    )
                    work_time.save()
            except Exception as err:
                print(err)
                pass
            try:
                for service_data in carwash_data.get("services"):
                    service = CarWashServicesModel(
                        carwash=carwash,
                        service=ServicesModel.objects.get_or_create(
                            name=service_data["title"]
                        )[0],
                        price=service_data["price"]
                    )
                    service.save()
            except Exception as err:
                print(err)
                pass
