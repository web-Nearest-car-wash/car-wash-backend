from rest_framework.serializers import ModelSerializer

from carwash.models import CarWashModel


class CarWashCardSerializer(ModelSerializer):
    """Сериализатор для карточки мойки"""
    class Meta:
        fields = '__all__'
        model = CarWashModel


class CarWashSerializer(ModelSerializer):
    """Сериализатор для вывода моек на главной странице"""
    class Meta:
        fields = '__all__'
        model = CarWashModel
