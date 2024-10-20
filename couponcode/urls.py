from django.urls import path
from .views import CouponListCreateAPIView, CouponDetailAPIView

urlpatterns = [
    path('coupons/', CouponListCreateAPIView.as_view(), name='coupon-list-create'),
    path('coupons/<int:coupon_id>/', CouponDetailAPIView.as_view(), name='coupon-detail'),

]
