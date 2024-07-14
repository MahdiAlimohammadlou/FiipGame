from django.urls import path
from .views import top_players, PlayerView, BuyBusinessView, UpgradeBusinessView

urlpatterns = [
    path('top-players/', top_players, name='top-players'),
    path('player/', PlayerView.as_view(), name='player'),
    path('buy-business/', BuyBusinessView.as_view(), name='buy-business'),
    path('upgrade-business/', UpgradeBusinessView.as_view(), name='upgrade-business'),
]