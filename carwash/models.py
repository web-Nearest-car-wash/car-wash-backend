from django.core.validators import RegexValidator
from django.db import models


class CarWashType(models.Model):
    name = models.CharField("Тип автомойки", blank=True, null=False,
                            max_length=200)

    class Meta:
        verbose_name = "Тип автомойки"
        verbose_name_plural = "Типы автомоек"

    def __str__(self):
        return f'{self.name}'


class CarWash(models.Model):
    name = models.CharField("Название", null=False, blank=True,
                            max_length=200)
    coordinates = models.CharField(
        "Координаты Ш,Д",
        blank=True,
        max_length=200,
        validators=[
            RegexValidator(
                regex=("^-?([0-8]?[0-9]|90)(\.[0-9]{1,10}),"
                       "([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$"),
                message='Неверные координаты',
            ),
        ]
    )
    loyalty = models.TextField("Лояльность", null=True, default=None,
                               max_length=500)
    price_list = models.CharField("Прайс лист", null=True, default=None,
                                  max_length=500)
    legal_person = models.BooleanField("Работа с юр лицами", default=False)
    type = models.ForeignKey(CarWashType, verbose_name="Тип автомойки",
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Автомойка"
        verbose_name_plural = "Автомойки"

    def __str__(self):
        return f'{self.name}'
