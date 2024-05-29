from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Estate, Image
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from io import BytesIO
from PIL import Image as PilImage

class EstateCreateTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword', email="mksdlmslk@gmail.com")
        
        # Generate token for the test user
        self.token = RefreshToken.for_user(self.user).access_token
        
        # URL for creating estate
        self.url = reverse('create')

    def generate_image_file(self, name='test_image.png'):
        file = BytesIO()
        image = PilImage.new('RGB', (100, 100))
        image.save(file, 'PNG')
        file.name = name
        file.seek(0)
        return file

    def test_create_estate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        data = {
            'title': 'Test Estate',
            'description': 'This is a test estate.',
            'status': 'Available',
            'price': 1000000,
            'user': self.user.id,
            'images': [self.generate_image_file()]
        }

        response = self.client.post(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estate.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)
        estate = Estate.objects.get()
        self.assertEqual(estate.title, 'Test Estate')

