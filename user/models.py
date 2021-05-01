from django.db import models
from django.contrib.auth.models import User

class NetflixUser(models.Model):
    """Model for Netflix User Data"""
    netflix_login = models.CharField(max_length=255)
    netflix_profile = models.CharField(max_length=50)
    netflix_password = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Show(models.Model):
    """Show to be shared by the users"""
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)