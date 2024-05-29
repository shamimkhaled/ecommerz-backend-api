from django.urls import path, include
from rest_framework import routers
# from rest_framework.routers import DefaultRouter
from accounts.views import (UserAPIView, UserLoginAPIView, UserProfileAPIView,
                             UserLogoutAPIView, UserRegisterationAPIView)


# router = DefaultRouter()
# router.register(r'', UserAPIView)
# router.register(r'login', UserLoginAPIView)
# router.register(r'logout', UserLogoutAPIView)
# router.register(r'register', UserRegisterationAPIView)








urlpatterns = [
    # path('', include(router.urls)),
    path('', UserAPIView.as_view()),

    path('register', UserRegisterationAPIView.as_view(), name='register'),
	path('login', UserLoginAPIView.as_view(), name='login'),
	path('logout', UserLogoutAPIView.as_view(), name='logout'),
    path('profiles', UserProfileAPIView.as_view(), name='userprofile'),
    # path('profiles/<str:username>', UserProfileAPIView.as_view(), name='user-profile'),

   
 
]