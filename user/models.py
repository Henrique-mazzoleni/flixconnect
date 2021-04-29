from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Custom User Model"""
    username = models.CharField(max_length=50, unique=True)
    netflix_login = models.CharField(max_length=255)
    netflix_username = models.CharField(max_length=50)
    netflix_password = models.CharField(max_length=30)

    objects = UserManager()


class Show(models.Model):
    """Show to be shared by the users"""
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)