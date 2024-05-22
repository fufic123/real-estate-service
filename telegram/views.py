from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BotAdmin
from .serializers import BotAdminSerializer

@api_view(['GET'])
def bot_info(request):
    singleton_token = BotAdmin.load()
    serializer = BotAdminSerializer(singleton_token)
    return Response(serializer.data, status=status.HTTP_200_OK)
