from django.contrib import admin
from .models import *

@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    search_fields = ['title', 'user__username']
    filter_horizontal = ['accessabilities']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_at']
    search_fields = ['estate__title']

@admin.register(Accessability)
class AccessabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


admin.site.register(Type)