from rest_framework import serializers

from core.serializers import BaseSerializer
from .models import Player, PlayerBusiness
from asset.models import Business
from asset.serializers import BusinessSerializer


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

class PlayerBusinessSerializer(BaseSerializer):
    business_detail = serializers.SerializerMethodField()

    class Meta:
        model = PlayerBusiness
        fields = [
            "id", "player", "level", "profit", "business", "business_detail"
        ]

    def get_business_detail(self, obj):
        queryset = Business.objects.filter(id=obj.business_id)
        business = queryset.first()
        serializer = BusinessSerializer(instance=business, context={"url": self.url})
        return serializer.data