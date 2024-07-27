from django.urls import path
from .views import top_players, PlayerView, ListBusinessesView, BuyBusinessView, UpgradeBusinessView

urlpatterns = [
    path('top-players/', top_players, name='top-players'),
    path('player/', PlayerView.as_view(), name='player'),
    path('businesses/', ListBusinessesView.as_view(), name='list_businesses'),
    path('businesses/buy/<int:business_id>/', BuyBusinessView.as_view(), name='buy_business'),
    path('businesses/upgrade/<int:business_id>/', UpgradeBusinessView.as_view(), name='upgrade_business'),
]