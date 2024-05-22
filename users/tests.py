from django.test import TestCase
from .models import User

class UserModelTests(TestCase):
    def test_create_user(self):
        # Test creating a regular user
        user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            name='John',
            surname='Doe'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.surname, 'Doe')
        self.assertEqual(user.username, 'John Doe')
        self.assertIsNotNone(user.ref_code)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_confirmed_requirements)
        self.assertTrue(user.is_confirmed_news)

    def test_create_superuser(self):
        # Test creating a superuser
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            name='Admin',
            surname='User'
        )
        
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('admin123'))
        self.assertEqual(admin_user.name, 'Admin')
        self.assertEqual(admin_user.surname, 'User')
        self.assertIsNotNone(admin_user.ref_code)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_confirmed_requirements)
        self.assertTrue(admin_user.is_confirmed_news)
