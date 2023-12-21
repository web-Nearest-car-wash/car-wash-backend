from rest_framework.serializers import (FloatField, ModelSerializer,
                                        ReadOnlyField, SerializerMethodField)

from carwash.models import CarWashModel, CarWashServicesModel, CarWashTypeModel


class CarWashTypeSerializer(ModelSerializer):
    """Сериализатор для типа мойки"""
    class Meta:
        fields = ('name',)
        model = CarWashTypeModel


class CarWashServicesSerializer(ModelSerializer):
    """
    Сериализатор для услуг мойки
    """
    name = ReadOnlyField(
        source='service.name', read_only=True
    )
    description = ReadOnlyField(
        source='service.description', read_only=True
    )

    class Meta:
        fields = ('name', 'description', 'price')
        model = CarWashServicesModel


class CarWashCardSerializer(ModelSerializer):
    """Сериализатор для карточки мойки"""
    type = CarWashTypeSerializer()
    rating = FloatField(read_only=True)
    services = SerializerMethodField()

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'services')
        model = CarWashModel

    def get_services(self, obj):
        queryset = obj.carwashservicesmodel_set.all()
        return CarWashServicesSerializer(queryset, many=True).data


class CarWashSerializer(ModelSerializer):
    """Сериализатор для вывода моек на главной странице"""
    type = CarWashTypeSerializer()
    rating = FloatField(read_only=True)
    services = SerializerMethodField()

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'services')
        model = CarWashModel

    def get_services(self, obj):
        queryset = obj.carwashservicesmodel_set.all()
        return CarWashServicesSerializer(queryset, many=True).data
