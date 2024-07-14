from django.urls import path
from .consumers import BusinessConsumer

websocket_urlpatterns = [
    path('ws/business/', BusinessConsumer.as_asgi()),
]