from django.urls import path, include
from rest_framework.routers import DefaultRouter




urlpatterns = [

    path('accounts/', include('accounts.urls')),
    path('', include('store.urls')),
    path('', include('cart.urls')),
    path('', include('couponcode.urls')),
    path('', include('order.urls')),
    path('', include('payment.urls')),
    path('', include('product_utils.urls')),




]