from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserAccount, UserProfile
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response


model = get_user_model()

#     class Meta:
#         model = UserAccount
#         fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superadmin']

# ========================UserRegisterationSerializer===============================
class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})


    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "password", ]

    def create(self, validated_data):
        user_password = validated_data.get('password', None)
        db_instance = self.Meta.model(
            first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'),
            username=validated_data.get('username'), email=validated_data.get('email')
            
            )
        db_instance.set_password(user_password)
        db_instance.save()

        return db_instance

# ========================UserLoginSerializer===============================
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
      



# ========================UserProfileSerializer===============================
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "username", "user_image", "address", "city", "country","zip_code", "phone"]

        def get_user(self, obj):
            user = obj.user
            return {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email
            }


# ========================UserAccountSerializer===============================
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'





# ========================PasswordResetRequestSerializer===============================
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError('No user is associated with this email address.')
        return value
    
# ========================PasswordResetConfirmSerializer===============================
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data