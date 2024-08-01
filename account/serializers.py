from rest_framework import serializers

from core.serializers import BaseSerializer
from .models import (Player, PlayerBusiness, PlayerCryptocurrency, PlayerProperty,
                      PlayerStock, PlayerVehicle, PlayerItem, Avatar)
from asset.models import Business, Cryptocurrency, Property, Stock, Vehicle
from asset.serializers import (BusinessSerializer, CryptocurrencySerializer, PropertySerializer,
                                StockSerializer, VehicleSerializer)
from avatar_customization.models import Item
from avatar_customization.serializers import ItemSerializer
from core.utils import get_full_url

class TopPlayerSerializer(BaseSerializer):

    class Meta:
        model = Player
        fields = ["profit", "coin", "level"]

class AvatarSerializer(BaseSerializer):
    avatar_image_full_url = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = [
            "id", "name", "gender", "avatar_image_full_url"
        ]

    def get_avatar_image_full_url(self, obj):
        if obj.avatar_image:
            return get_full_url(obj, 'avatar_image', self.url)
        return None

class PlayerSerializer(BaseSerializer):
    avatar_detail = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
        "user", "profit", "coin", "level", "referral_code", "last_coin_update", "avatar_detail"
        ]

    def get_avatar_detail(self, obj):
        queryset = Avatar.objects.get(id=obj.avatar.id)
        serializer = AvatarSerializer(instance=queryset, context={"url": self.url})
        return serializer.data

class PlayerCreateSerializer(BaseSerializer):
    class Meta:
        model = Player
        fields = ['avatar']

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

class PlayerBusinessSerializer(BaseSerializer):
    business_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerBusiness
        fields = [
            "id", "player", "level", "profit", "business", "business_detail"
        ]

    def get_business_detail(self, obj):
        queryset = Business.objects.get(id=obj.business_id)
        serializer = BusinessSerializer(instance=queryset, context={"url": self.url})
        return serializer.data
    
class PlayerCryptocurrencySerializer(BaseSerializer):
    cryptocurrency_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerCryptocurrency
        fields = [
            "id", "player", "cryptocurrency", "quantity", "cryptocurrency_detail"
        ]

    def get_cryptocurrency_detail(self, obj):
        queryset = Cryptocurrency.objects.get(id=obj.cryptocurrency.id)
        serializer = CryptocurrencySerializer(instance=queryset, context={"url": self.url})
        return serializer.data
    
class PlayerPropertySerializer(BaseSerializer):
    property_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerProperty
        fields = [
                "id", "player", "property", "property_detail"
        ]

    def get_property_detail(self, obj):
        queryset = Property.objects.get(id=obj.property.id)
        serializer = PropertySerializer(instance=queryset, context={"url": self.url})
        return serializer.data
    
class PlayerStockSerializer(BaseSerializer):
    stock_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerStock
        fields = [
                "id", "player", "stock", "quantity", "stock_detail"
        ]

    def get_stock_detail(self, obj):
        queryset = Stock.objects.get(id=obj.stock.id)
        serializer = StockSerializer(instance=queryset, context={"url": self.url})
        return serializer.data
    
class PlayerVehicleSerializer(BaseSerializer):
    vehicle_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerVehicle
        fields = [
                "id", "player", "vehicle", "vehicle_detail"
        ]

    def get_vehicle_detail(self, obj):
        queryset = Vehicle.objects.get(id=obj.vehicle.id)
        serializer = VehicleSerializer(instance=queryset, context={"url": self.url})
        return serializer.data
    
class PlayerItemSerializer(BaseSerializer):
    item_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerItem
        fields = [
                "id", "player", "item", "is_active", "item_detail"
        ]

    def get_item_detail(self, obj):
        queryset = Item.objects.get(id=obj.item.id)
        serializer = ItemSerializer(instance=queryset, context={"url": self.url})
        return serializer.data