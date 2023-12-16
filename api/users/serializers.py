from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CustomUserCreateSerializer(UserCreateSerializer):
    username = serializers.RegexField(
        max_length=150, regex=r'^[\w.@+-]+\Z', required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
