from django.urls import path
from .views import *

urlpatterns = [
    path("bot-admin/", bot_info)
]
