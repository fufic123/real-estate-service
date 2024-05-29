from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.exceptions import ValidationError
from django.conf import settings

import os

from .models import Estate, Image, Accessability
from .serializers import EstateSerializer, AccessabilitySerializer

class CreateEstateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = EstateSerializer(data=data)
        if serializer.is_valid():
            try:
                estate = serializer.save()

                images = request.FILES.getlist('images')
                if len(images) + estate.images.count() > 20:
                    return Response({"error": "Cannot upload more than 20 images."}, status=status.HTTP_400_BAD_REQUEST)

                for image in images:
                    img = Image.objects.create(image=image)
                    estate.images.add(img)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEstateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
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


class DeleteEstateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request):
        pk = request.data["id"]
        try:
            estate = Estate.objects.get(pk=pk, user=request.user)
            images = estate.images.all()
            for image in images:
                image_path = f"{settings.MEDIA_ROOT}/{image.image}"
                if os.path.exists(image_path):
                    os.remove(image_path)
            estate.delete()
            return Response({"message": "Estate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Estate.DoesNotExist:
            return Response({"error": "Estate not found or not owned by user."}, status=status.HTTP_404_NOT_FOUND)


class UploadImagesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        pk = request.data["id"]
        try:
            estate = Estate.objects.get(pk=pk, user=request.user)
        except Estate.DoesNotExist:
            return Response({"error": "Estate not found or not owned by user."}, status=status.HTTP_404_NOT_FOUND)
        
        images = request.FILES.getlist('images')
        if len(images) + estate.images.count() > 20:
            return Response({"error": "Cannot upload more than 20 images."}, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            img = Image.objects.create(image=image)
            estate.images.add(img)

        return Response({"message": "Images uploaded successfully."}, status=status.HTTP_200_OK)


class DeleteImagesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request):
        image_ids = request.data.get('ids', [])
        
        if not image_ids:
            return Response({"error": "No image IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        images = Image.objects.filter(id__in=image_ids, estate__user=request.user)
        
        if not images.exists():
            return Response({"error": "No images found for the provided IDs"}, status=status.HTTP_404_NOT_FOUND)
        
        for image in images:
            image_path = f"{settings.MEDIA_ROOT}/{image.image}"
            if os.path.exists(image_path):
                os.remove(image_path)
            image.delete()

        return Response({"message": "Images deleted successfully"}, status=status.HTTP_200_OK)


class EstatesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        queryset = Estate.objects.filter(user=user)
        serializer = EstateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EstateInfoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        pk = request.data["id"]
        try:
            estate = Estate.objects.get(pk=pk)
        except Estate.DoesNotExist:
            return Response({"error": "Estate not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EstateSerializer(estate)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccessabilitiesView(APIView):
    def get(self, request):
        queryset = Accessability.objects.all()
        serializer = AccessabilitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
