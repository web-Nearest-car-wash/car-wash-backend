from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from multiselectfield import MultiSelectField

from core.constants import PAYMENT_CHOICES, SCORES
from services.models import ServicesModel
from users.models import User


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
    latitude = models.DecimalField(
        verbose_name='Широта',
        blank=False, null=False,
        max_digits=8,
        decimal_places=6,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    longitude = models.DecimalField(
        verbose_name='Долгота',
        blank=False,
        null=False,
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'
        constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude'],
                                    name='unique_metro_coordinates')
        ]

    def __str__(self):
        return f'{self.name}'


class CarWashModel(models.Model):
    """Модель автомойки."""
    name = models.CharField(verbose_name='Название', null=False, blank=False,
                            max_length=200)
    latitude = models.DecimalField(
        verbose_name='Широта',
        blank=False, null=False,
        max_digits=8,
        decimal_places=6,
        default='55.558741',
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    longitude = models.DecimalField(
        verbose_name='Долгота',
        blank=False,
        null=False,
        max_digits=9,
        decimal_places=6,
        default='37.378847',
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )
    legal_person = models.BooleanField(
        verbose_name='Работа с юридическими лицами',
        default=False
    )
    loyalty = models.TextField(verbose_name="Лояльность", null=True,
                               blank=True, max_length=500)

    type = models.ForeignKey(CarWashTypeModel, verbose_name='Тип автомойки',
                             on_delete=models.SET_NULL, null=True)
    metro = models.ManyToManyField(
        MetroStationModel,
        through='NearestMetroStationModel',
        verbose_name='Ближайшие станции метро.')
    service = models.ManyToManyField(
        ServicesModel,
        through='CarWashServicesModel',
        verbose_name='Оказываемые услуги'
    )
    rest_room = models.BooleanField(
        verbose_name='Комната отдыха',
        default=False,
        help_text='Наличие комнаты отдыха'
    )
    payment = MultiSelectField(
        verbose_name='Способ оплаты',
        choices=PAYMENT_CHOICES,
        max_choices=4,
        null=True,
        blank=True,
        help_text='Выберите способ оплаты',
        max_length=30
    )
    over_information = models.TextField(
        max_length=1000,
        verbose_name='Дополнительная информация',
        null=True, blank=True
    )

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
    metro_station = models.ForeignKey(
        MetroStationModel,
        verbose_name='Станция метро',
        on_delete=models.CASCADE
    )
    distance = models.PositiveIntegerField(
        verbose_name='Расстояние до автомойки',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Ближайшая станция метро'
        verbose_name_plural = 'Ближайшие станции метро'
        constraints = [
            models.UniqueConstraint(
                fields=['carwash', 'metro_station'],
                name='unique_carwash_metro')
        ]

    def __str__(self):
        return f'{self.carwash} рядом с метро {self.metro_station}'


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

    class Meta:
        verbose_name = 'Цена услуги'
        verbose_name_plural = 'Цены услуг'

    def __str__(self):
        return f'{self.service.name}, {self.service.description}, {self.price}'


class CarWashRatingModel(models.Model):
    score = models.IntegerField(
        verbose_name='Оценка',
        choices=SCORES
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        null=True, blank=True
    )
    carwash = models.ForeignKey(
        CarWashModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Оценка автомойки'
        verbose_name_plural = 'Оценки автомоек'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('carwash', 'user'),
                name='unique_carwash_user'
            )
        ]

    def __str__(self):
        return f'{self.score}'
