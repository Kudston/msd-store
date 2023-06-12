from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Products
from django.forms import ModelForm

class userCreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class user_loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProductCreationForm(ModelForm):
    last_updated = forms.DateTimeField(initial=datetime.utcnow, disabled=True)
    class Meta:
        model = Products
        fields = ['name', 'quantity', 'unit_price', 'last_updated']
