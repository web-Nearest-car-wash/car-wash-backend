from math import cos, radians, sin

from django.db.models import ExpressionWrapper, F, FloatField, Func

from core.constants import EARTH_AVERAGE_RADIUS


def distance_calculation(queryset, latitude, longitude):
    """Добавление поля расстояние в queryset.
    Рассчет расстояния до указанных координат от кадой автомойки,
    сортировка по расстоянию"""
    return queryset.annotate(
            distance=ExpressionWrapper(
                EARTH_AVERAGE_RADIUS * Func(
                    Func(
                        Func(F('latitude'), function='RADIANS'),
                        function='SIN'
                    )*sin(
                        radians(latitude)
                    ) + Func(
                        Func(F('latitude'), function='RADIANS'),
                        function='COS'
                    )*cos(radians(latitude))*Func(
                        Func(
                            F('longitude'), function='RADIANS'
                        )-radians(longitude),
                        function='COS'
                    ), function='ACOS'
                ),
                output_field=FloatField()
            ),
        ).order_by('distance')
