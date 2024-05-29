from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Estate
from telegram.utils.promotion import send_promotion
from telegram.utils.get_username import get_username
import threading
import os

@receiver(post_save, sender=Estate)
def send_promotion_message(sender, instance, created, **kwargs):
    if created:
        try:
            images = list(instance.images.all()[:9])

            message = ""
            message += f"{instance.title}\n\n"
            message += f"{instance.description}\n\n"
            message += f"Status: {instance.status}\n"
            message += f"Price: {instance.price}\n"
            
            try:
                user = instance.user
                channel = get_username(user.telegram)
            except:
                return "User did not set up telegram channel or group link."
            
            # Start a new thread to send the promotion message
            thread = threading.Thread(target=send_promotion, args=(message, channel, *images))
            thread.start()
            
        except Exception as e:
            print(f"Error sending telegram message: {e}")
