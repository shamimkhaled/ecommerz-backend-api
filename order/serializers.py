from rest_framework import serializers
from .models import Orders, OrderItem, Shipping
from cart.models import Carts, CartItem
from cart.serializers import CartSerializer, CartItemSerializer




class ShippingCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'name', 'rate', 'estimated_delivery_days']
        

class OrderItemSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_variation', 'quantity', 'price', 'sub_total']


    def get_sub_total(self, obj):
        return obj.sub_total()

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    order_status = serializers.SerializerMethodField(read_only=True)

    cart = serializers.CharField()
    shipping_cost = serializers.ChoiceField(choices=Shipping.objects.values_list('name', flat=True).distinct())  
    total_amount = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    # grand_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    

    class Meta:
        model = Orders
        fields = ['order_id', 'user', 'cart', 'order_status', 'shipping_address', 'orderitems',  'total_amount',  'shipping_cost', 'grand_total', 'order_placed_at']


    def get_user(self, obj):
        user = obj.user
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email
        }
    
    def get_total_amount(self, obj):
        return obj.total_amount

    def get_grand_total(self, obj):
        return obj.grand_total
    
    def get_order_status(self, obj):
        return obj.order_status
    

    
    def update(self, instance, validated_data):
        # Update only the allowed fields
        instance.status = validated_data.get('status', instance.status)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.shipping_cost = validated_data.get('shipping_cost', instance.shipping_cost)
        instance.save()
        return instance
    


