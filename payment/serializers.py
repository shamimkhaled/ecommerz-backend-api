from rest_framework import serializers
from .models import Payment
from order.models import Orders
from order.serializers import OrderSerializer
import datetime


def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")

def check_expiry_year(value):
    today = datetime.datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")

def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(max_length=150, required=True, validators=[check_expiry_month])
    expiry_year = serializers.CharField(max_length=150, required=True, validators=[check_expiry_year])
    cvc = serializers.CharField(max_length=150, required=True, validators=[check_cvc])




class PaymentSerializer(serializers.ModelSerializer):
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'payment_method', 'amount', 'transaction_id', 'payment_status', 'grand_total', 'created_at', 'update_at']
        read_only_fields = ['id', 'user', 'transaction_id', 'amount', 'payment_status', 'grand_total', 'created_at', 'update_at']
    
    # order = OrderSerializer()


    def get_grand_total(self, obj):
        
        order = obj.order  # Access the related order field directly
        if order:
            return order.grand_total
        # return obj.order.grand_total
        return 0

    
    def get_user(self, obj):
        user = obj.user
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        payment = Payment.objects.create(**validated_data)
        return payment
