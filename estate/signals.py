from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Estate
from tg.utils.promotion import run_promotion_thread
from tg.utils.get_username import get_username
import os
from django.db import transaction
import threading

@receiver(post_save, sender=Estate)
def send_promotion_message(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_promotion_after_commit(instance))

def send_promotion_after_commit(instance):
    try:
        instance_images = instance.images.all()
        if not instance_images:
            print("No images found for the estate.")
            return

        images = [image.image.url for image in instance_images]

        message = ""
        message += f"{instance.title}\n\n"
        message += f"{instance.description}\n\n"
        message += f"Status: {instance.status}\n"
        message += f"Price: {instance.price}\n"

        try:
            user = instance.user
            channel = get_username(user.telegram)
        except Exception as e:
            print("User did not set up telegram channel or group link.")
            return

        # Send the promotion message with images
        thread = threading.Thread(target=run_promotion_thread, args=(message, channel, *images))
        thread.start()  

    except Exception as e:
        print(f"Error sending telegram message: {e}, {channel}")