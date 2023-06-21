from django.db import models
import uuid
from datetime import datetime
# Create your models here.
class Products(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=225, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.FloatField()
    last_updated = models.DateTimeField(default=datetime.now)
    last_time_sold = models.DateTimeField(null=True, default=datetime.now)
     
    def __str__(self):
      return self.name
      
class Sells(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=225)
    quantity = models.PositiveIntegerField(null=True, default=0)
    cost = models.FloatField()
    date_sold = models.DateTimeField(null=False, default=datetime.now)
    order = models.ForeignKey('Order', null=True, on_delete=models.SET_NULL)
    def __str__(self):
      return self.product_name
      
class Adds(models.Model):
      id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
      product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
      product_name = models.CharField(max_length=225)
      quantity = models.PositiveIntegerField()
      date_added = models.DateTimeField(null=False, default=datetime.now)
      def __str__(self):
        return self.product_name
  
class Order(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    order_time = models.DateTimeField(null=False, default=datetime.now)
    def __str__(self):
      return str(self.order_time)
      