from rest_framework import serializers
from .models import BotAdmin

class BotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotAdmin
        fields = ['icon', 'name', 'url']
