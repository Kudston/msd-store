from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Products
from django.forms import ModelForm

class user_loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProductCreationForm(ModelForm):
    last_updated = forms.DateTimeField(initial=datetime.now, disabled=True)
    class Meta:
        model = Products
        fields = ['name', 'unit_price', 'last_updated']
        
class NewUserForm(UserCreationForm):
  registration_token = forms.CharField()
  class Meta:
    model = User
    fields = ("username", "email","password1", "password2", "registration_token")
  def save(self, commit=True):
	  user = super(NewUserForm, self).save(commit=False)
	  user.email = self.cleaned_data['email']
	  if commit:
	    user.save()
	    return user