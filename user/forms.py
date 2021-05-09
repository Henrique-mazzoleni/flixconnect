from django.forms import ModelForm
from .models import NetflixUser

class NetflixUserForm(ModelForm):
    class Meta:
        model = NetflixUser
        fields = ['login', 'password', 'profile']