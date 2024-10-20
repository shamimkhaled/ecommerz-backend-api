from django.db import models
from accounts.models import *
from store.models import *
from django.template.defaultfilters import default, slugify

# Create your models here.



class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f'Review for {self.product.product_title} by {self.user.username}'
    

# =================================Wishlist========================
class Wishlist(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Products, related_name='wishlists')
    # slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f'Wishlist of {self.user.username}'
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.products.product_title)
    #     return super().save(*args, **kwargs)


# ===================================Compare=====================
class Compare(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='compare')
    products = models.ManyToManyField(Products, related_name='compares')
    
    def __str__(self):
        return f'Comparison list of {self.user.username}'