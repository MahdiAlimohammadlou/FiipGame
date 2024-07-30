from rest_framework import serializers

from core.serializers import BaseSerializer
from core.utils import get_full_url
from .models import Business, Cryptocurrency, Property, Stock, Vehicle

class BusinessSerializer(BaseSerializer):
    image_abs_url = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = [
          "id", "name", "base_profit", "cost", "upgrade_cost_factor", "category", "ranking", "description", "image_abs_url"
        ]
    
    def get_image_abs_url(self, obj):
        if obj.business_image:
            return get_full_url(obj, 'business_image', self.url)
        return None

class CryptocurrencySerializer(BaseSerializer):
    currency_logo_abs_url = serializers.SerializerMethodField()

    class Meta:
        model = Cryptocurrency
        fields = [
          "id", "name", "price", "purchasable_quantity", "currency_logo_abs_url",
        ]
    
    def get_currency_logo_abs_url(self, obj):
        if obj.currency_logo:
            return get_full_url(obj, 'currency_logo', self.url)
        return None

class PropertySerializer(BaseSerializer):
    property_img_abs_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
          "id", "name", "price", "property_img_abs_url",
        ]
    
    def get_property_img_abs_url(self, obj):
        if obj.property_img:
            return get_full_url(obj, 'property_img', self.url)
        return None

class StockSerializer(BaseSerializer):
    stock_logo_abs_url = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
          "id", "name", "price", "purchasable_quantity", "stock_logo_abs_url",
        ]
    
    def get_stock_logo_abs_url(self, obj):
        if obj.stock_logo:
            return get_full_url(obj, 'stock_logo', self.url)
        return None

class VehicleSerializer(BaseSerializer):
    vehicle_img_abs_url = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
          "id", "name", "price", "vehicle_type", "vehicle_img_abs_url",
        ]
    
    def get_vehicle_img_abs_url(self, obj):
        if obj.vehicle_img:
            return get_full_url(obj, 'vehicle_img', self.url)
        return None