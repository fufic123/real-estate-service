
from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateEstateView.as_view(), name='create'),
    path('update/', UpdateEstateView.as_view(), name='update'),
    path('delete/', DeleteEstateView.as_view(), name='delete'),
    path('upload-images/', UploadImagesView.as_view(), name='upload-images'),
    path('delete-images/', DeleteImagesView.as_view(), name='delete-images'),
    path('', EstatesView.as_view(), name='estates'),
    path('info/', EstateInfoView.as_view(), name='estate-info'),
    path('accessabilities/', AccessabilitiesView.as_view(), name='accessabilities'),
]