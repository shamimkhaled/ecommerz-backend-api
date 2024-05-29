from django.shortcuts import render
from .models import UserAccount, UserProfile
from .serializers import  UserRegisterationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from .token import generate_access_token
from django.shortcuts import get_object_or_404
from django.http import Http404
from .token_authentication import CustomTokenAuthentication
import jwt




# Create your views here.
# class UserAccountViewSet(viewsets.ModelViewSet):
#     queryset = UserAccount.objects.all()
#     serializer_class = UserAccountSerializer


# ========================UserRegisterationAPIView===============================
class UserRegisterationAPIView(APIView):
    serializer_class = UserRegisterationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = {'access_token': access_token}
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
        
    

# ========================UserLoginAPIView===============================
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', None)
        user_password = request.data.get('password', None)

        if not user_password:
            raise AuthenticationFailed('An user password is required.')

        if not email:
            raise AuthenticationFailed('An user email is required.')

        user_instance = authenticate(username=email, password=user_password)

        if not user_instance:
            raise AuthenticationFailed('User not found.')

        if user_instance.is_active:
            user_access_token = generate_access_token(user_instance)
            response = Response()
            response.set_cookie(key='access_token', value=user_access_token, httponly=True)
            response.data = {
                'message': 'Login successfully.',
                'access_token': user_access_token
            }
            return response

        return Response({
            'message': 'Incorrect Credentials.'
        })


# ========================UserLogoutAPIView===============================
class UserLogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token', None)
        if user_token:
            response = Response()
            response.delete_cookie('access_token')
            response.data = {
                'message': 'Logged out successfully.'
            }
            return response
        response = Response()
        response.data = {
            'message': 'User is already logged out.'
        }
        return response



# ========================UserAPIView===============================
class UserAPIView(APIView):
    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        model = get_user_model()
        user = model.objects.filter(user_id=payload['user_id']).first()
        serializer_class = UserRegisterationSerializer(user)
        return Response(serializer_class.data)
    

# ========================UserProfileAPIView===============================
class UserProfileAPIView(APIView):


    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (AllowAny,)

    # def get_object(self, username):
    #     try:
    #         username = self.kwargs['username']
    #         return UserProfile.objects.get(user__username=username)
    #     except UserProfile.DoesNotExist:
    #         raise Http404

    # def get(self, request, username):
    #     user_token = request.COOKIES.get('access_token')

    #     if not user_token:
    #         raise AuthenticationFailed('Unauthenticated user.')

    #     payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

    #     model = get_user_model()
    #     user = model.objects.filter(user_id=payload['user_id']).first()
    #     if user.username != username:
    #         raise AuthenticationFailed('User is not authorized to access this profile.')

    #     profile = self.get_object(username)
    #     serializer_class = UserProfileSerializer(profile)
    #     return Response(serializer_class.data)
    

    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        model = get_user_model()
        user = model.objects.filter(user_id=payload['user_id']).first()
        profile = user.userprofile
        serializer_class = UserProfileSerializer(profile)
        return Response(serializer_class.data)
   


    