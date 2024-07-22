from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
import jwt
from account.models import User

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.using('main_service').get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        authorization_header = headers.get(b'authorization', None)

        if authorization_header:
            try:
                # Extract token from the 'JWT ' prefix
                token = authorization_header.decode().split(' ')[1]
                # Decode and validate the token
                decoded_token = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
                user_id = decoded_token['user_id']
                scope['user'] = await get_user(user_id)
            except jwt.ExpiredSignatureError:
                # Token has expired
                scope['user'] = AnonymousUser()
            except jwt.DecodeError:
                # Token decoding failed
                scope['user'] = AnonymousUser()
            except jwt.InvalidTokenError:
                # Invalid token
                scope['user'] = AnonymousUser()
            except IndexError:
                # Malformed token
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
