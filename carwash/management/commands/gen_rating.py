from random import choices, randint

from django.core.management import BaseCommand

from carwash.models import CarWashRatingModel, CarWashModel


class Command(BaseCommand):
    help = "Generates ratings for existing carwashes"

    def handle(self, *args, **options):
        carwashes = CarWashModel.objects.all()
        choices_scores = [3, 4, 5]

        for carwash in carwashes:
            try:
                number_scores = randint(0, 10)
                for _ in range(number_scores):
                    score = choices(choices_scores)[0]
                    CarWashRatingModel.objects.create(
                        score=score, carwash=carwash
                    )
            except Exception as err:
                print(err)
                continue
