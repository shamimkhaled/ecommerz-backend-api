from django.shortcuts import render
from accounts.models import UserAccount, UserProfile
from .serializers import  (UserRegisterationSerializer, UserLoginSerializer,
                           PasswordResetConfirmSerializer, PasswordResetRequestSerializer, UserProfileSerializer)
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse
from .serializers import PasswordResetRequestSerializer
import jwt



# ========================UserRegisterationAPIView===============================
class UserRegisterationAPIView(APIView):
    serializer_class = UserRegisterationSerializer
    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = {'access_token': access_token, 'message': 'Account created successfully'}
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
        
    

# ========================UserLoginAPIView===============================
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (CustomTokenAuthentication,)
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
    authentication_classes = (CustomTokenAuthentication,)
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

    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user

        if not user:
            raise AuthenticationFailed('User not Found.')


        profile = user.userprofile
        serializer_class = UserProfileSerializer(profile)
        return Response(serializer_class.data)
    
    
class UpdateUserProfileAPIView(generics.UpdateAPIView):
    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        user = self.request.user
        if not user:
            raise AuthenticationFailed('User not found.')
        return user.userprofile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'message': 'Profile updated successfully.',
                'data': serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ========================PasswordResetView===============================

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = UserAccount.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construct password reset URL
        reset_url = request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )
        
        # Send email
        subject = 'Password Reset Requested'
        message = f"""
        Hello {user.username},

        You're receiving this email because you requested a password reset for your user account at our site.

        Please go to the following page and choose a new password:
        {reset_url}

        Your username, in case you’ve forgotten: {user.username}

        Thanks for using our site!
        """
        send_mail(subject, message, None, [user.email])
        msg = {'message': 'Password reset link are already sent in email'},
        
        return Response( {'reset_url': reset_url, 'message': msg}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserAccount.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        

