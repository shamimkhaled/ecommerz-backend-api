from django.urls import path
from .views import CartListCreateAPIView, CartDetailAPIView, CartItemListCreateAPIView, CartItemDetailAPIView, ApplyCouponCodeView

urlpatterns = [
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('carts/<uuid:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart-items/', CartItemListCreateAPIView.as_view(), name='cartitem-list-create'),
    path('cart-items/<int:pk>/', CartItemDetailAPIView.as_view(), name='cartitem-detail'),
    path('carts/<uuid:cart_id>/apply-coupon/', ApplyCouponCodeView.as_view(), name='apply-coupon'),

]
