from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Products,
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
  
class loginFormSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
      
class ProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Products
    fields = '__all__'