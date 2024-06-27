from django.urls import path
from .views import top_players, RetrievePlayerView, CreatePlayerView

urlpatterns = [
    path('top-players/', top_players, name='top-players'),
    path('player/<str:device_id>/', RetrievePlayerView.as_view(), name='retrieve-player'),
    path('player/', CreatePlayerView.as_view(), name='create-player'),
]