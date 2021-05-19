from django.db import models
from django.contrib.auth.models import User

class NetflixUser(models.Model):
    """Model for Netflix User Data"""
    login = models.CharField(max_length=255)
    profile = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile

class Show(models.Model):
    """Show to be shared by the users"""
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title