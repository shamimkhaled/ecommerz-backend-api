from django.urls import path
from .views import *
from .views import ( PaymentStatusUpdateView, PaymentCreateViewAPI, 
                    PaymentFormView, CreateCheckoutSessionStripeView, PaymentSuccessView, PaymentCancelView)
from . import views

urlpatterns = [
    path('create-payments/', PaymentCreateViewAPI.as_view(), name='create-payment'),
    path('payments/<int:pk>/', PaymentStatusUpdateView.as_view(), name='payment-status-update'),

    path('make-payment/', PaymentFormView.as_view()),
    path('create-checkout-session/', CreateCheckoutSessionStripeView.as_view(), name='create-checkout-session'),

    path('payments/success', PaymentSuccessView.as_view(), name='payment-success'),
    path('payments/cancel', PaymentCancelView.as_view(), name='payment-cancel'),

    path('ssl-payments/initiate/', CreateSSLCommerzSessionView.as_view(), name='create_sslcommerz_session'),
    path('ssl-payments/success/', SSLCommerzSuccessView.as_view(), name='sslcommerz_success'),
    path('ssl-payments/fail/', SSLCommerzFailView.as_view(), name='sslcommerz_fail'),
    path('ssl-payments/cancel/', SSLCommerzCancelView.as_view(), name='sslcommerz_cancel'),
    path('ssl-payments/ipn/', SSLCommerzIPNView.as_view(), name='sslcommerz_ipn'),

]
