from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserAuthMaster(AbstractUser):
    username = models.CharField(max_length=50,unique=True)
    phonenumber = models.CharField(max_length=20)
    email=models.EmailField()
    profile_image = models.ImageField(upload_to='Userprofile',blank=True,null=True)
    password=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    last_login=models.DateTimeField(auto_now_add=True)
    forgot_token = models.CharField(editable=False,default="")
    forgot_token_expiration = models.DateTimeField(null=True,blank=True,editable=False)
    
    def __str__(self):
        return self.username