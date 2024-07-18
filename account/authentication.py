from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings
from .models import User
import jwt

class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        try:
            # Decode the token
            decoded_token = jwt.decode(raw_token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        except jwt.ExpiredSignatureError:
            raise InvalidToken('Token has expired')
        except jwt.DecodeError:
            raise InvalidToken('Error decoding token')

        # Validate the user in the service one database
        try:
            user = User.objects.using('main_service').get(id=decoded_token['user_id'])
            if not user.is_active:
                raise InvalidToken('User is inactive')
        except User.DoesNotExist:
            raise InvalidToken('User not found')

        return super().get_validated_token(raw_token)

    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        try:
            user = User.objects.using('main_service').get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        return user
