from django.urls import path
from .views import BusinessView, CryptocurrencyView, PropertyView, StockView, VehicleView

urlpatterns = [
    #Business
    path('businesses/', BusinessView.as_view(), name='businesses-list'),
    #Crypto
    path('cryptocurrencies/', CryptocurrencyView.as_view(), name='cryptocurrency'),
    #Property
    path('properties/', PropertyView.as_view(), name='property'),
    #Stock
    path('stocks/', StockView.as_view(), name='stock'),
    #Vehicle
    path('vehicles/', VehicleView.as_view(), name='vehicle'),
]