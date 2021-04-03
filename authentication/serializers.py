# Helper link
"""
 JwtEg: https://medium.com/analytics-vidhya/django-rest-api-with-json-web-token-jwt-authentication-69536c01ee18
 JwtSnippet:https://vimsky.com/zh-tw/examples/detail/python-method-rest_framework.authentication.get_authorization_header.html
JWPpage: https://styria-digital.github.io/django-rest-framework-jwt/
https://pypi.org/project/django-rest-passwordreset/
"""

import datetime
from abc import ABC

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(max_length=300, use_url=True, allow_null=True, required=False)

    class Meta:
        model = UserProfile
        # fields = '__all__'
        fields = ('id', 'phone_number', "age", "gender", 'image_url')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']

        )
        return user


class UserSignInSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            refresh = RefreshToken.for_user(user)
            jwt_token = refresh.access_token
            # expiry = datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA

            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        serializer_data = {
            'email': user.email,
            'token': jwt_token,

        }

        return serializer_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
