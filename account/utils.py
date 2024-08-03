from .models import (PlayerBusiness, PlayerCryptocurrency, PlayerItem,
                      PlayerProperty, PlayerStock, PlayerVehicle)

def get_player_business_cost(player):
    businesses = PlayerBusiness.objects.filter(player=player)
    if not businesses.exists():
        return 0
    return sum(
        business.business.cost * (business.business.upgrade_cost_factor ** level)
        for business in businesses
        for level in range(1, business.level)
    )

def get_player_crypto_cost(player):
    cryptos = PlayerCryptocurrency.objects.filter(player=player)
    if not cryptos.exists():
        return 0
    return sum(
        crypto.quantity * crypto.cryptocurrency.price 
        for crypto in cryptos
    )

def get_player_property_cost(player):
    properties = PlayerProperty.objects.filter(player=player)
    if not properties.exists():
        return 0
    return sum(
        property.property.price
        for property in properties
    )

def get_player_stock_cost(player):
    stocks = PlayerStock.objects.filter(player=player)
    if not stocks.exists():
        return 0
    return sum(
        stock.quantity * stock.stock.price 
        for stock in stocks
    )

def get_player_vehicle_cost(player):
    vehicles = PlayerVehicle.objects.filter(player=player)
    if not vehicles.exists():
        return 0
    return sum(
        vehicle.vehicle.price 
        for vehicle in vehicles
    )

def get_player_item_cost(player):
    items = PlayerItem.objects.filter(player=player)
    if not items.exists():
        return 0
    return sum(
        item.item.price 
        for item in items
    )
