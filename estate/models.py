from django.db import models

from django.core.exceptions import ValidationError

from users.models import User

# Create your models here.
class Image(models.Model):
    estate = models.ForeignKey('Estate', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='estate_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Accessability(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Estate(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title", default="New estate", null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name="Description", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estates')
    accessabilities = models.ManyToManyField(Accessability, related_name='estates', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:            
            if self.images.count() > 20:
                raise ValidationError("Cannot upload more than 20 images.")
            super().save(*args, **kwargs)