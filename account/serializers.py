from rest_framework import serializers
from .models import Player, Business, PlayerBusiness

class TopPlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ["name", "profit", "coin", "level"]

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = [
          "name", "profit", "coin", "level", "referral_code", "last_coin_update"
        ]