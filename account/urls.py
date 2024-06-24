from django.urls import path
from .views import top_players, player_by_device_id

urlpatterns = [
    path('top-players/', top_players, name='top-players'),
    path('player/<str:device_id>/', player_by_device_id, name='player-by-device-id'),
]