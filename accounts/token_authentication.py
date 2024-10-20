from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
# from .models import UserAccount

class CustomTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            return None  # No token means the user is anonymous

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        model = get_user_model()
        user = model.objects.filter(user_id=payload['user_id']).first()        
        # user = model.objects.get(user_id=payload['user_id'])
        
        
        if not user:
            raise AuthenticationFailed('User not found.')

        return (user, None)
