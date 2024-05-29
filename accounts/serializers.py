from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserAccount, UserProfile
from django.contrib.auth import get_user_model


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


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'