from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    """Custom User Model"""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255)
    netflix_login = models.CharField(max_length=255)
    netflix_username = models.CharField(max_length=50)
    netflix_password = models.CharField(max_length=30)


class Show(models.Model):
    """Show to be shared by the users"""
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    user = models.Foreignkey(User, on_delete=models.CASCADE)