from django.db import models
import uuid
from datetime import datetime
# Create your models here.
class Products(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=225, unique=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField()
    last_updated = models.DateTimeField(default=datetime.utcnow)
    last_time_sold = models.DateTimeField(null=True)
class Sells(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=225)
    quantity = models.PositiveIntegerField()
    cost = models.FloatField()
    date_sold = models.DateTimeField(null=False)
  
class Adds(models.Model):
      id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
      product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
      product_name = models.CharField(max_length=225)
      quantity = models.PositiveIntegerField()
      date_added = models.DateTimeField(null=False)