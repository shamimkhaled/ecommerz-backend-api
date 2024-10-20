from django.db import models
from order.models import Orders, OrderItem
from accounts.models import UserAccount
from payment.models import Payment
import uuid
# from rest_framework.permissions import BasePermission


# Create your models here.
class RefundItems(models.Model):
    refund = models.ForeignKey('Refunds', on_delete=models.CASCADE, related_name='refund_items')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Refunds(models.Model):
    # refund_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='refunds')
    transaction_id = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')

    reason = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ], default='PENDING')
    requested_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, related_name='requested_refunds')  # User who requested
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, related_name='processed_refunds')  # User who processed
    processed_at = models.DateTimeField(null=True, blank=True)

    # class Meta:
    #     permissions = [
    #         ("can_process_refund", "Can process refunds"),
    #     ]

    def __str__(self):
        return f'Refund for Order {self.order.order_id}'
    
    # def save(self, *args, **kwargs):

    #     self.transaction_id = self.transaction_id.transaction_id
    #     super().save(*args, **kwargs)


    
    # def get_transaction_id(self):
    #     return self.transaction_id.transaction_id
