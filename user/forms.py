from django import forms

class NetflixUserForm(forms.Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='access_pass', max_length=30)
    profile = forms.CharField(label='profile', max_length=50)