from django.core.validators import RegexValidator
from django.db import models

from services.models import ServicesModel


class CarWashTypeModel(models.Model):
    """Модель типа автомойки."""
    name = models.CharField(verbose_name='Тип автомойки', blank=False,
                            null=False, max_length=200, unique=True)

    class Meta:
        verbose_name = "Тип автомойки"
        verbose_name_plural = "Типы автомоек"

    def __str__(self):
        return f'{self.name}'


class MetroStationModel(models.Model):
    """Модель станции метро."""
    name = models.CharField(verbose_name='Название', null=False, blank=False,
                            max_length=200)
    latitude = models.CharField(
        verbose_name='Широта',
        blank=False, null=False,
        max_length=13,
        validators=[
            RegexValidator(
                regex=('^-?([0-8]?[0-9]|90)(\.[0-9]{1,10})$'),
                message='Неверное указание широты, '
                        'должно быть вида 55.752378',
            ),
        ]
    )
    longitude = models.CharField(
        verbose_name='Долгота',
        blank=False,
        null=False,
        max_length=14,
        validators=[
            RegexValidator(
                regex=('^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$'),
                message='Неверное указание долготы, '
                        'должно быть вида 55.752378',
            ),
        ]
    )

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'
        constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude'],
                                    name='unique_metro_coordinates')
        ]


class CarWashModel(models.Model):
    """Модель автомойки."""
    name = models.CharField(verbose_name='Название', null=False, blank=False,
                            max_length=200)
    latitude = models.CharField(
        verbose_name='Широта',
        blank=False, null=False,
        max_length=13,
        validators=[
            RegexValidator(
                regex=('^-?([0-8]?[0-9]|90)(\.[0-9]{1,10})$'),
                message='Неверное указание широты, '
                        'должно быть вида 55.752378',
            ),
        ]
    )
    longitude = models.CharField(
        verbose_name='Долгота',
        blank=False,
        null=False,
        max_length=14,
        validators=[
            RegexValidator(
                regex=('^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$'),
                message='Неверное указание долготы, '
                        'должно быть вида 55.752378',
            ),
        ]
    )
    legal_person = models.BooleanField(
        verbose_name='Работа с юридическими лицами',
        default=False
    )
    loyalty = models.TextField(verbose_name="Лояльность", null=True,
                               blank=True, max_length=500)

    type = models.ForeignKey(CarWashTypeModel, verbose_name='Тип автомойки',
                             on_delete=models.CASCADE)
    metro = models.ManyToManyField(
        MetroStationModel,
        through="NearestMetroStationModel",
        verbose_name="Ближайшие станци метро.")
    service = models.ManyToManyField(
        ServicesModel,
        through="CarWashServicesModel",
        verbose_name="Оказываемые услуги"
    )
    over_information = models.TextField(max_length=1000, verbose_name="Доолнительная информация")

    class Meta:
        verbose_name = 'Автомойка'
        verbose_name_plural = 'Автомойки'
        constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude'],
                                    name='unique_car_wash_coordinates')
        ]

    def __str__(self):
        return f'{self.name}'


class NearestMetroStationModel(models.Model):
    """Промежуточная модель связи станции метро и автомойки."""
    carwash = models.ForeignKey(CarWashModel, verbose_name='Автомойка',
                                on_delete=models.CASCADE)
    metrostation = models.ForeignKey(
        MetroStationModel,
        verbose_name='Станция метро',
        on_delete=models.CASCADE
    )
    distance = models.IntegerField(verbose_name='Расстояние до автомойки',
                                   blank=True, null=True)


class CarWashImageModel(models.Model):
    """Модель для фотографий для автомойки."""
    carwash = models.ForeignKey(CarWashModel, verbose_name='Автомойка',
                                on_delete=models.CASCADE)
    image = models.URLField(verbose_name='Фото автомойки')
    avatar = models.BooleanField(verbose_name='На аватарку', default=False)

    class Meta:
        verbose_name = 'Фотография автомойки'
        verbose_name_plural = 'Фотографии автомойки'

    def __str__(self):
        return f'Фото с id {self.id} к автомойке "{self.carwash.name}".'


class CarWashServicesModel(models.Model):
    """Модель для цен на услуги автомойки."""
    carwash = models.ForeignKey(CarWashModel, verbose_name='Автомойка',
                                on_delete=models.CASCADE)
    service = models.ForeignKey(ServicesModel, verbose_name='Услуга',
                                on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена', blank=True, null=True)


class PromotionsModel(models.Model):
    """Модель акции автомойки."""
    carwash = models.ForeignKey(CarWashModel, verbose_name='Автомойка',
                                on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Акция автомойки'
        verbose_name_plural = 'Акции автомойки'

    def __str__(self):
        return f'{self.text[:150]}'
