from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    """Show to be shared by the users"""
    title = models.CharField(max_length=255)
    link = models.CharField(max_lenght=255)
    user = models.Foreignkey(User, on_delete=models.CASCADE)