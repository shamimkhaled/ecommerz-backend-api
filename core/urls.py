from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns



urlpatterns = [

    path('accounts/', include('accounts.urls')),
    path('', include('store.urls')),
    path('', include('cart.urls')),
    path('', include('couponcode.urls')),
    path('', include('order.urls')),
    path('', include('payment.urls')),
    path('', include('product_utils.urls')),
    path('', include('refund.urls')),
    path('dashboard/', include('dashboard.urls')),







]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)