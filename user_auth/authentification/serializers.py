from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User

from django.contrib.auth import authenticate

from rest_framework.exceptions import AuthenticationFailed


class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)



    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'birthdate',
        )

    def create(self, validated_data):
        account = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            birthdate=validated_data.get('birthdate')
        )
        return account


class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=60)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('Не удалось войти в аккаунт.')
        user_tokens = user.tokens()
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }

    class Meta:
        model = User
        fields = (
            "email", "password", "access_token", "refresh_token",
        )

