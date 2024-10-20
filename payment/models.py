from django.db import models
from django.conf import settings
from order.models import Orders
from accounts.models import UserAccount


# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=100, choices=[
        ('cash_on_delivery', 'Cash On Delivery'),
        ('stripe', 'Stripe'),
        ('sslcommerz', 'SSLCommerz'),
        ('bkash', 'bKash'),
        
    ], default='cash_on_delivery')
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f"{self.user.username} - {self.order.order_id} - {self.payment_status}"
        return f"{self.transaction_id} - {self.payment_status} - {self.user.username}  "



class BillingAddress(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.TextField(max_length=200, blank=True, null=True)
    address2 = models.TextField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s billing address"

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True