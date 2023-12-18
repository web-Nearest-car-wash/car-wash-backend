from rest_framework.serializers import ModelSerializer

from carwash.models import CarWashModel, CarWashTypeModel


class CarWashTypeSerializer(ModelSerializer):
    """Сериализатор для типа мойки"""
    class Meta:
        fields = ('name',)
        model = CarWashTypeModel


class CarWashCardSerializer(ModelSerializer):
    """Сериализатор для карточки мойки"""
    type = CarWashTypeSerializer()
    class Meta:
        fields = '__all__'
        model = CarWashModel


class CarWashSerializer(ModelSerializer):
    """Сериализатор для вывода моек на главной странице"""
    class Meta:
        fields = '__all__'
        model = CarWashModel
