from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):  ## Inherit from django form and add more fields
    email = forms.EmailField()         ## Add email field to form 
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]    ## Order of display on form
    