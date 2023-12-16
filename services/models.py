from django.db import models


class ServicesModel(models.Model):
    """Модель для оказываемых услуг."""
    name = models.CharField(verbose_name='Услуга', blank=False,
                            null=False, max_length=200, unique=True)
