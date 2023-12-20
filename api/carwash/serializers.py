from rest_framework.serializers import FloatField, ModelSerializer

from carwash.models import CarWashModel, CarWashTypeModel


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


class CarWashSerializer(ModelSerializer):
    """Сериализатор для вывода моек на главной странице"""
    type = CarWashTypeSerializer()
    rating = FloatField(read_only=True)

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'service')
        model = CarWashModel
