from django.contrib import admin
from .models import Shipping, Orders, OrderItem

# Register your models here.

admin.site.register([Shipping, Orders, OrderItem])