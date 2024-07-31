from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from account.models import (Player, PlayerItem) 
from account.serializers import (PlayerItemSerializer)
from .models import Item
from .serializers import ItemSerializer
from core.exceptions import NotEnoughMoney, ItemDoesNotExist

        
class ItemManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        if action == 'buy':
            return self.buy_item(request)
        elif action == 'select':
            return self.select_item(request)
        else:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        player = get_object_or_404(Player, user=request.user.id)

        # Get purchased items
        purchased_items = PlayerItem.objects.filter(player=player.id)
        purchased_items_data = PlayerItemSerializer(purchased_items, many=True, context={"request":request}).data

        # Get unpurchased items
        purchased_item_ids = purchased_items.values_list('item_id', flat=True)
        unpurchased_items = Item.objects.exclude(id__in=purchased_item_ids)
        unpurchased_items_data = ItemSerializer(unpurchased_items, many=True, context={"request":request}).data

        # Return response with both purchased and unpurchased items
        return Response({
            'purchased_items': purchased_items_data,
            'unpurchased_items': unpurchased_items_data
        })

    def buy_item(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        item_id = request.data.get('item_id')

        if not item_id or not player:
            return Response({'error': 'Item ID and Player ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise ItemDoesNotExist()

        try:
            if player.coin < item.price:
                raise NotEnoughMoney()

            # Deduct item price from player's coins
            player.coin -= item.price
            player.save()

            PlayerItem.objects.create(player=player, item=item)
            return Response({'status': 'Item purchased successfully.'}, status=status.HTTP_201_CREATED)
        except NotEnoughMoney as e:
            return Response({'error': str(e)}, status=status.HTTP_402_PAYMENT_REQUIRED)
        except Player.DoesNotExist:
            return Response({'error': 'Player does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def select_item(self, request):
        player_item_id = request.data.get('player_item_id')

        if not player_item_id:
            return Response({'error': 'PlayerItem ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            player_item = PlayerItem.objects.get(id=player_item_id)
            player = player_item.player
            item = player_item.item

            # Deselect any active item of the same category type
            PlayerItem.objects.filter(
                player=player, 
                item__category_type=item.category_type, 
                is_active=True
            ).update(is_active=False)

            # Select the new item
            player_item.is_active = True
            player_item.save()

            return Response({'status': 'Item selected successfully.'}, status=status.HTTP_200_OK)
        except PlayerItem.DoesNotExist:
            return Response({'error': 'PlayerItem does not exist.'}, status=status.HTTP_404_NOT_FOUND)
