# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Estate
# from telegram.utils.send_promotion import send_telegram_message

# @receiver(post_save, sender=Estate)
# def send_promotion_message(sender, instance, created, **kwargs):
#     if created:
#         try:
#             images = list(instance.images.all()[:9])

#             message = ""
#             message += f"{instance.title}\n\n"
#             message += f"{instance.description}\n\n"
#             message += f"Status: {instance.status}\n"
#             message += f"Price: {instance.price}\n"

#             send_telegram_message(message, images, instance.user)
#         except Exception as e:
#             print(f"Error sending telegram message: {e}")
