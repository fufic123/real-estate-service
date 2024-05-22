from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import *
class EstateModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@example.com',
            password='password123',
            name='Owner',
            surname='Estate'
        )
        self.etype = Type.objects.create(name='Apartment')
        self.accessability = Accessability.objects.create(name='Elevator')

    def test_create_estate(self):
        estate = Estate.objects.create(
            title='Beautiful Estate',
            description='A beautiful estate with a nice view.',
            user=self.user,
            etype=self.etype,
            location='123 Estate Ave',
            price=1000000.00,
            status='active',
            stype='for_sale'
        )
        estate.accessabilities.add(self.accessability)
        self.assertEqual(estate.title, 'Beautiful Estate')
        self.assertEqual(estate.user, self.user)
        self.assertEqual(estate.etype, self.etype)
        self.assertEqual(estate.status, 'active')
        self.assertEqual(estate.stype, 'for_sale')
        self.assertIn(self.accessability, estate.accessabilities.all())

    def test_image_upload_limit(self):
        estate = Estate.objects.create(
            title='Limited Estate',
            user=self.user,
            etype=self.etype,
            location='456 Estate Blvd',
            price=500000.00
        )
        for i in range(20):
            Image.objects.create(estate=estate, image=f'image_{i}.jpg')
        
        with self.assertRaises(ValidationError):
            Image.objects.create(estate=estate, image='image_21.jpg')
            estate.save()
