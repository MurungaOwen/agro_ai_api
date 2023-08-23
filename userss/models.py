from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(_("email"),unique=True)
    phone_number=PhoneNumberField(_(" phone number"),region="KE",unique=True)
    region=models.CharField(max_length=30,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def clean_phone(self):
        if len(self.phone_number)<10:
            raise ValueError(_("length of phone number is invalid"))
        return self.phone_number
# # 
# class Details(models.Model):
#     phone_number=models.OneToOneField(User,)
    
