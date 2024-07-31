from rest_framework import serializers

from core.serializers import BaseSerializer
from .models import Item

class ItemSerializer(BaseSerializer):

    class Meta:
        model = Item
        fields = [
            "id", "name", "category_type", "price", "description",
        ]