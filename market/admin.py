from django.contrib import admin
from .models import Products, Sells, Adds, Order
# Register your models here.
admin.site.register(Products)
admin.site.register(Sells)
admin.site.register(Adds)
admin.site.register(Order)