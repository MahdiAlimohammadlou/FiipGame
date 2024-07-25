import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from .middlewares import JWTAuthMiddleware
from account import routing as account_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FiipGame.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": 
                # JWTAuthMiddleware(
                    URLRouter(
                        account_routing.websocket_urlpatterns
                    )
                # )
    }
)