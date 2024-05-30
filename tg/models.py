from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"An instance of {self.__class__.__name__} already exists.")
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(f"Deletion of {self.__class__.__name__} instance is not allowed.")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class BotAdmin(SingletonModel):
    icon = models.ImageField(upload_to="tgbot/", null=True, blank=True, verbose_name="Icon")
    name = models.CharField(max_length=50, verbose_name="Name")
    url = models.URLField(max_length=200, verbose_name="URL")
    token = models.CharField(max_length=255, unique=True, verbose_name="Token")

    class Meta:
        verbose_name = "TG Bot"
        verbose_name_plural = "TG Bot"

    def __str__(self):
        return self.token