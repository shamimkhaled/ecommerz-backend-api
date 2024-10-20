from django.urls import path
from .views import RefundRequestView, RefundProcessView

urlpatterns = [
    path('refund/request/', RefundRequestView.as_view(), name='refund-request'),
    path('refund/request/<int:pk>/', RefundRequestView.as_view(), name='refund-request'),

    path('refund/process/<int:pk>/', RefundProcessView.as_view(), name='refund-process'),
]
