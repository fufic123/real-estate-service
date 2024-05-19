
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.exceptions import ValidationError

from .models import *
from .serializers import EstateSerializer

from django.core.files.storage import default_storage

import os
from django.conf import settings


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@parser_classes([MultiPartParser, FormParser])
def create_estate(request):
    data = request.data.copy()
    data['user'] = request.user.id

    serializer = EstateSerializer(data=data)
    if serializer.is_valid():
        try:
            estate = serializer.save()
            
            images = request.FILES.getlist('images')
            if len(images) + estate.images.count() > 20:
                return Response({"error": "Cannot upload more than 20 images."}, status=status.HTTP_400_BAD_REQUEST)
            # Create Image objects for each uploaded image
            for image in images:
                Image.objects.create(estate=estate, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_estate(request):
    pk = request.data["id"]
    try:
        estate = Estate.objects.get(pk=pk, user=request.user)
    except Estate.DoesNotExist:
        return Response({"error": "Estate not found or not owned by user."}, status=status.HTTP_404_NOT_FOUND)

    serializer = EstateSerializer(estate, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_estate(request):
    pk = request.data["id"]
    try:
        estate = Estate.objects.get(pk=pk, user=request.user)
        images = estate.images
        for image in images:
            # Delete the file from the storage
            image_path = f"{settings.MEDIA_ROOT}/{image.image}"
            if os.path.exists(image_path):
                os.remove(image_path)
        estate.delete()
        return Response({"message": "Estate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Estate.DoesNotExist:
        return Response({"error": "Estate not found or not owned by user."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def upload_images(request):
    pk = request.data["id"]
    try:
        estate = Estate.objects.get(pk=pk, user=request.user)
    except Estate.DoesNotExist:
        return Response({"error": "Estate not found or not owned by user."}, status=status.HTTP_404_NOT_FOUND)
    
    images = request.FILES.getlist('images')
    if len(images) + estate.images.count() > 20:
        return Response({"error": "Cannot upload more than 20 images."}, status=status.HTTP_400_BAD_REQUEST)

    for image in images:
        Image.objects.create(estate=estate, image=image)

    return Response({"message": "Images uploaded successfully."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_images(request):
    image_ids = request.data.get('ids', [])
    
    if not image_ids:
        return Response({"error": "No image IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

    images = Image.objects.filter(id__in=image_ids, estate__user=request.user)
    
    if not images.exists():
        return Response({"error": "No images found for the provided IDs"}, status=status.HTTP_404_NOT_FOUND)
    
    for image in images:
        # Delete the file from the storage
        image_path = f"{settings.MEDIA_ROOT}/{image.image}"
        if os.path.exists(image_path):
            os.remove(image_path)
        # Delete the image record from the database
        image.delete()

    return Response({"message": "Images deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def estates(request):
    user = request.user
    queryset = Estate.objects.filter(user=user)
    serializer = EstateSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def estate_info(request):
    pk = request.data["id"]
    queryset = Estate.objects.get(pk=pk)
    serializer = EstateSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def accessabilities(request):
    queryset = Accessability.objects.all()
    serializer = AccessabilitySerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)