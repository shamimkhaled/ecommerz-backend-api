from rest_framework import serializers
from .models import Refunds, RefundItems
from order.models import OrderItem, Orders



class RefundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundItems
        fields = ['order_item', 'quantity']

class RefundSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Refund
    #     fields = ['id', 'order', 'reason', 'amount', 'status', 'requested_by', 'requested_at', 'processed_by', 'processed_at']
    #     read_only_fields = ['status', 'requested_by' ,'requested_at', 'processed_by', 'processed_at']

    refund_items = RefundItemSerializer(many=True, required=False)

    class Meta:
        model = Refunds
        fields = ['id', 'order', 'transaction_id', 'refund_items', 'reason', 'amount', 'status', 'requested_by', 'requested_at', 'processed_by', 'processed_at']
        read_only_fields = ['status', 'requested_by', 'requested_at', 'processed_by', 'processed_at']

    def create(self, validated_data):
        refund_items_data = validated_data.pop('refund_items', [])
        refund = super().create(validated_data)
        for item_data in refund_items_data:
            RefundItems.objects.create(refund=refund, **item_data)
        return refund
    
    # def get_transaction_id(self, obj):
    #     return obj.transaction_id.transaction_id

    



class RefundStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refunds
        fields = ['status', 'processed_by', 'processed_at']
        read_only_fields = ['processed_by', 'processed_at']

