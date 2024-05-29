# serializers.py
from rest_framework import serializers
from .models import Estate, Image, Accessability

class AccessabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessability
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class EstateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Estate
        fields = '__all__'
