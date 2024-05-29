from django.db import models

from django.core.exceptions import ValidationError

from users.models import User

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='estate_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Accessability(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "Accessability"
        verbose_name_plural = "Accessabilities"

class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Estate(models.Model):
    title = models.CharField(max_length=100, default="New estate", null=True, blank=True, verbose_name="Title")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estates', verbose_name="User",)
    accessabilities = models.ManyToManyField(Accessability, related_name='estates', blank=True, verbose_name="Accessabilities")
    images = models.ManyToManyField(Image, verbose_name="Images")
    etype = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, verbose_name="Property type")
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name="Property's address")
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name="Price")
    
    STATUS_CHOICES = [
        ("sold", "Sold"),
        ("active", "Active"),
        ("hot_offer", "Hot offer"),
        ("no_fees", "No fees"),
        ("reservated", "Reservated"),
        ("discount", "Discount")
    ]
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True, verbose_name="Status")
    
    STYPE_CHOICES = [
        ("for_sale", "For sale"),
        ("for_rent", "For rent")
    ]
    stype = models.CharField(max_length=50, choices=STYPE_CHOICES, null=True, blank=True, verbose_name="Sale or Rent")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:            
            if self.images.count() > 1:
                raise ValidationError("Cannot upload more than 20 images.")
            super().save(*args, **kwargs)