from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from account.models import Player
import uuid

@database_sync_to_async
def get_user_from_api_key(api_key):
    try:
        return Player.objects.get(api_key=api_key)
    except (Player.DoesNotExist, ValidationError):
        return AnonymousUser()

class APIKeyAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope['headers'])
        api_key_bytes = headers.get(b'api-key')

        if api_key_bytes:
            api_key_str = api_key_bytes.decode('utf-8')
            try:
                api_key = uuid.UUID(api_key_str)
                scope['user'] = await get_user_from_api_key(api_key)
            except ValueError:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
