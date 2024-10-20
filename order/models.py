import uuid
from django.db import models
from accounts.models import UserAccount
from store.models import Products, ProductVariation
from cart.models import Carts
from cart.serializers import CartSerializer

# Create your models here.


class Shipping(models.Model):
    name = models.CharField(max_length=250)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_days = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    



class Orders(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.PROTECT, related_name='orders')
    cart = models.OneToOneField(Carts, on_delete=models.CASCADE, related_name='order')
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    shipping_cost = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    grand_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=100, choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')
    shipping_address = models.TextField()

    order_placed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     self.total_amount = sum(item.sub_total() for item in self.cart.cartitems.all())
    #     if self.cart.coupon:
    #         discount = ( self.total_amount * self.cart.coupon.discount) / 100
    #         self.total_amount -= discount

    #     if self.shipping_cost:
    #         self.grand_total = self.total_amount + self.shipping_cost.rate
    #     else:
    #         self.grand_total = self.total_amount
    #     super().save(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.pk:
            # Calculate the total_amount and grand_total when the order is first created
            self.total_amount = sum(item.sub_total() for item in self.cart.cartitems.all())
            if self.cart.coupon:
                discount = (self.total_amount * self.cart.coupon.discount) / 100
                self.total_amount -= discount
            self.grand_total = self.total_amount + self.shipping_cost.rate
        super(Orders, self).save(*args, **kwargs)


   


    def __str__(self):
        return f"{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.product_variation:
            self.price = self.product_variation.price
        else:
            self.price = self.product.price
        super().save(*args, **kwargs)


    def sub_total(self):
        if self.product_variation:
            return self.product_variation.price * self.quantity
        else:
            return self.product.price * self.quantity


    def __str__(self):
        return f"{self.order.order_id} - {self.product.product_title} - {self.price}"