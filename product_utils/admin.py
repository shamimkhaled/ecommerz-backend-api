from django.contrib import admin
from .models import Review, Wishlist
# Register your models here.

admin.site.register([Review, Wishlist])


