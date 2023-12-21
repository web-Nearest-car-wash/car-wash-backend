from rest_framework.serializers import FloatField, ModelSerializer

from carwash.models import CarWashModel, CarWashTypeModel
from .utils import cut_zeros


class CarWashTypeSerializer(ModelSerializer):
    """Сериализатор для типа мойки"""
    class Meta:
        fields = ('name',)
        model = CarWashTypeModel


class CarWashCardSerializer(ModelSerializer):
    """Сериализатор для карточки мойки"""
    type = CarWashTypeSerializer()
    rating = FloatField(read_only=True)

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'service')
        model = CarWashModel

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        return cut_zeros(serializer)


class CarWashSerializer(ModelSerializer):
    """Сериализатор для вывода моек на главной странице"""
    type = CarWashTypeSerializer()
    rating = FloatField(read_only=True)

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'service')
        model = CarWashModel

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        return cut_zeros(serializer)
