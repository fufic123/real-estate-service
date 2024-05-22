from django.contrib import admin
from django.urls import path, include

from .views import documentation


urlpatterns = [
    path('docs/', documentation),
    
    #APIS
    path('user/', include("users.urls")),
    path('estate/', include("estate.urls")),
    path('tg/', include("telegram.urls"))
]
