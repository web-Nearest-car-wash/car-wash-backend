from django_filters.rest_framework import CharFilter, FilterSet


from carwash.models import CarWashModel


class CarWashFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = CarWashModel
        fields = ('name',)
