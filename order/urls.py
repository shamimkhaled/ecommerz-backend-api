from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, OrderListViewSet, OrderDetailViewSet, OrderUpdateView

urlpatterns = [
    path('orders/', OrderViewSet.as_view(), name='order-create'),
    path('order-list/', OrderListViewSet.as_view(), name='order-create'),

    path('orders/<uuid:pk>/', OrderDetailViewSet.as_view(), name='order-detail'),
    path('orders/<uuid:pk>/update/', OrderUpdateView.as_view(), name='order-update'),


    path('orders/<uuid:pk>/items/', OrderItemViewSet.as_view(), name='order-items-list'),

]

