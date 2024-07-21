from rest_framework import serializers

from core.serializers import BaseSerializer
from core.utils import get_full_url
from .models import Player, Business, PlayerBusiness

class TopPlayerSerializer(BaseSerializer):

    class Meta:
        model = Player
        fields = ["profit", "coin", "level"]

class PlayerSerializer(BaseSerializer):

    class Meta:
        model = Player
        fields = [
        "user", "profit", "coin", "level", "referral_code", "last_coin_update", "avatar"
        ]

class PlayerCreateSerializer(BaseSerializer):
    class Meta:
        model = Player
        fields = ['avatar']

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

class BusinessSerializer(BaseSerializer):
    image_abs_url = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = [
          "id", "name", "base_profit", "cost", "upgrade_cost_factor", "category", "ranking", "image_abs_url"
        ]
    
    def get_image_abs_url(self, obj):
        return get_full_url(obj, 'business_image', self.url)


class PlayerBusinessSerializer(BaseSerializer):
    class Meta:
        model = PlayerBusiness
        fields = [
          "id", "player", "business", "level", "profit"
        ]