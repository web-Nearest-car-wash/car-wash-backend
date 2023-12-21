from rest_framework.serializers import FloatField, ModelSerializer

from carwash.models import (CarWashModel, CarWashTypeModel, CarWashImageModel,
                            NearestMetroStationModel)


class CarWashImageSerializer(ModelSerializer):
    """Сериализатор для аватарки мойки."""

    class Meta:
        fields = ('image',)
        model = CarWashImageModel


class CarWashTypeSerializer(ModelSerializer):
    """Сериализатор для типа мойки."""

    class Meta:
        fields = ('name',)
        model = CarWashTypeModel


class NearestMetroStationSerializer(ModelSerializer):
    """Сериализатор для станции метро, ближайшей к автомойке."""

    class Meta:
        fields = ('name',)
        model = NearestMetroStationModel


class CarWashCardSerializer(ModelSerializer):
    """Сериализатор для карточки мойки."""

    rating = FloatField(read_only=True)
    type = CarWashTypeSerializer()

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'service')
        model = CarWashModel


class CarWashSerializer(ModelSerializer):
    """Сериализатор для вывода моек на главной странице."""

    image = CarWashImageSerializer()
    metro = NearestMetroStationSerializer()
    rating = FloatField(read_only=True)
    type = CarWashTypeSerializer()

    class Meta:
        fields = ('id', 'type', 'name', 'rating',
                  'latitude', 'longitude', 'loyalty',
                  'over_information', 'metro', 'service', 'image')
        model = CarWashModel
