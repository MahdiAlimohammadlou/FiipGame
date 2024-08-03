from django.urls import path
from .views import top_players, PlayerView, tap_count, get_values

urlpatterns = [
    path('top-players/', top_players, name='top-players'),
    path('player/', PlayerView.as_view(), name='player'),
    path('tap/', tap_count, name='tap'),
    path('get-values/', get_values, name='get-values'),
]