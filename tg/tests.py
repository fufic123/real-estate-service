from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import BotAdmin

class BotAdminModelTests(TestCase):
    def test_singleton_creation(self):
        bot_admin = BotAdmin.objects.create(
            icon='icon.jpg',
            name='Test Bot',
            url='https://example.com',
            token='sometoken123'
        )
        with self.assertRaises(ValidationError):
            BotAdmin.objects.create(
                icon='icon2.jpg',
                name='Test Bot 2',
                url='https://example2.com',
                token='anothertoken456'
            )
        
        self.assertEqual(BotAdmin.load(), bot_admin)

    def test_singleton_deletion(self):
        bot_admin = BotAdmin.objects.create(
            icon='icon.jpg',
            name='Test Bot',
            url='https://example.com',
            token='sometoken123'
        )
        with self.assertRaises(ValidationError):
            bot_admin.delete()
