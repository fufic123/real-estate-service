from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

import random
import string

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        # if not password:
        #     raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, surname=None, email=None, username=None, password=None, **extra_fields):
    # def create_user(self, *args):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        
        if username is None and name is not None and surname is not None:
            username = f"{name.capitalize()} {surname.capitalize()}"
        
        return self._create_user(email, password, name=name, surname=surname, username=username, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # General
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Avatar", null=True, blank=True, default=None)
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name="Username")
    email = models.EmailField(db_index=True, unique=True, max_length=254, verbose_name='Email')
    
    #Own
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="First name")
    surname = models.CharField(max_length=50, null=True, blank=True, verbose_name="Second name")
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name="Office's address")

    #Business
    website = models.URLField(max_length=500, null=True, blank=True, verbose_name="Website")
    instagram = models.URLField(max_length=500, null=True, blank=True, verbose_name="Instagram")
    facebook = models.URLField(max_length=500, null=True, blank=True, verbose_name="Facebook")
    
    telegram_chat_id = models.CharField(max_length=30, null=True, blank=True, verbose_name="Telegram Chat ID")
    
    #Technical
    is_active = models.BooleanField(default=True,
                                    verbose_name='Active')  # must needed, otherwise you won't be able to loginto django-admin.
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Staff')  # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False,
                                       verbose_name='Admin')  # this field we inherit from PermissionsMixin.
    ref_code = models.CharField(max_length=10, verbose_name="Referal code", unique=True, null=True, blank=True)
    
    is_confirmed_requirements = models.BooleanField(default=True, verbose_name="Confirmed terms")
    is_confirmed_news = models.BooleanField(default=True, verbose_name="Confirmed receiving emails")

    def save(self, *args, **kwargs):
        if not self.ref_code:
            ref_code_length = 8
            characters = string.ascii_letters + string.digits
            self.ref_code = ''.join(random.choices(characters, k=ref_code_length))
        super(User, self).save(*args, **kwargs)

    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name', 'surname', ]
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email if self.email else 'email not confirmed'
