from django import froms

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=30)
    login = forms.CharField(label='login', max_length=100)
    access_pass = forms.CharField(label='access_pass', max_length=30)
    profile = forms.CharField(label='profile', max_length=50)
