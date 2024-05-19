from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class AccessabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessability
        fields = ['name']

class EstateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    accessabilities = serializers.PrimaryKeyRelatedField(queryset=Accessability.objects.all(), many=True, required=False)

    class Meta:
        model = Estate
        fields = "__all__"

    def create(self, validated_data):
        accessabilities = validated_data.pop('accessabilities', [])
        images_data = validated_data.pop('images', [])
        estate = Estate.objects.create(**validated_data)
        if accessabilities:
            estate.accessabilities.set(accessabilities)
        for image_data in images_data:
            Image.objects.create(estate=estate, **image_data)
        return estate
