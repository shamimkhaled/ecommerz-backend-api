from django.db import models
from accounts.models import *
from store.models import *
from couponcode.models import Coupon
# Create your models here.

class Carts(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    products = models.ManyToManyField(Products, through='CartItem')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cart_id}"
    
    # def get_total_price(self, cart):
    #     total = sum(item.sub_total() for item in cart.cartitems.all())
    #     if cart.coupon:
    #         discount = (total * self.coupon.discount) / 100
    #         total -= discount
    #     return total
    
    def apply_coupon(self, coupon):
        if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.active:
            self.coupon = coupon
            self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  

    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        if self.product_variation:
            return self.product_variation.price * self.quantity
        else:
            return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} X {self.product}"
