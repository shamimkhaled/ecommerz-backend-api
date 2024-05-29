from rest_framework import serializers
from .models import  Coupon



class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'valid_from', 'valid_to', 'discount', 'active']

    
class ApplyCouponSerializers(serializers.ModelSerializer):
    coupon_code = serializers.CharField(max_length=15)

    class Meta:
        model = Coupon
        fields = ['coupon_code']
