from django.urls import path
from .views import top_players, PlayerView, tap_count

urlpatterns = [
    path('top-players/', top_players, name='top-players'),
    path('player/', PlayerView.as_view(), name='player'),
    path('tap/', tap_count, name='tap'),
]