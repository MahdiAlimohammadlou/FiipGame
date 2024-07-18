from rest_framework import serializers
from .models import Player, Business, PlayerBusiness

class TopPlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ["name", "profit", "coin", "level"]

class PlayerSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Player
        fields = [
          "name", "profit", "coin", "level", "referral_code", "last_coin_update"
        ]

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['avatar']

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
          "id", "name", "base_profit", "cost", "upgrade_cost_factor", "category", "ranking"
        ]

class PlayerBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerBusiness
        fields = [
          "id", "player", "business", "level", "profit"
        ]