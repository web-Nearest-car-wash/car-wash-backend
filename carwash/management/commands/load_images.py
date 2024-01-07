import json


import requests
import tempfile

from django.core import files

from carwash.models import CarWashImageModel, CarWashModel


class Command(BaseCommand):
    help = "Loads data from json"

    def handle(self, *args, **options):

        with open("data/data_output.json", encoding='utf-8') as f:
            json_data = json.load(f)
        carwashes_data = json_data.get("car_washes")

        for carwash_data in carwashes_data:
            if "photos" in carwash_data:
                for image in carwash_data["photos"][:3]:
                    # Stream the image from the url
                    image_url = image["photo_url"].split('%s')[0] + "XL"

                    # Get the filename from the url, used for saving later
                    file_name = image_url.split('/')[-2] + ".jpg"
                    carwash = CarWashModel.objects.filter(
                        latitude=carwash_data["latitude"][0],
                        longitude=carwash_data["longitude"][0]
                    ).first()
                    if not carwash or CarWashImageModel.objects.filter(
                            carwash=carwash,
                            image="carwash/" + file_name
                    ).exists():
                        continue

                    response = requests.get(image_url, stream=True)

                    # Was the request OK?
                    if response.status_code != requests.codes.ok:
                        # Nope, error handling, skip file etc etc etc
                        continue

                    # Create a temporary file
                    lf = tempfile.NamedTemporaryFile()

                    # Read the streamed image in sections
                    for block in response.iter_content(1024 * 8):

                        # If no more file then stop
                        if not block:
                            break

                        # Write image block to temporary file
                        lf.write(block)

                    # Create the model you want to save the image to
                    try:
                        car_wash_image = CarWashImageModel()
                        car_wash_image.carwash = carwash
                        car_wash_image.avatar = image["avatar"]
                        car_wash_image.image.save(file_name, files.File(lf))
                        car_wash_image.save()
                        print("изображение добавлено")
                    except Exception as err:
                        print(err)
                        continue
