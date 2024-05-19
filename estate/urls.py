
from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_estate, name='create_estate'),
    path('update/', update_estate, name='update_estate'),
    path('delete/', delete_estate, name='delete_estate'),
    path('upload-images/', upload_images, name='upload_images'),
    path('delete-images/', delete_images, name="delete_images"),
    path("", estate_info, name="estate_info"),
    path("all/", estates, name="estates"),
    path("accessabilities/", accessabilities, name="accessabilities")
]