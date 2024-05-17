from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            surname=validated_data['surname'],
            email=validated_data['email'],
            is_confirmed_requirements=validated_data['is_confirmed_requirements'],
            is_confirmed_news=validated_data['is_confirmed_news'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()
        return user