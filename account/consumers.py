import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Business, PlayerBusiness
from .serializers import Player

class BusinessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # user = self.scope.get('user', None)
        # self.player = await sync_to_async(Player.objects.get)(user=user.id)
        self.player = await sync_to_async(Player.objects.get)(id=8)
        await self.accept()
        await self.list_businesses()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action', None)
        business_id = data.get('business_id', None)

        if action == 'buy':
            await self.buy_business(business_id)
        elif action == 'upgrade':
            await self.upgrade_business(business_id)
        elif action == 'list':
            await self.list_businesses()

    async def buy_business(self, business_id):
        business = await sync_to_async(Business.objects.get)(id=business_id)
        success = await sync_to_async(self.player.buy_business)(business)
        await self.send(json.dumps({
            'action': 'buy',
            'business_id': business_id,
            'success': success
        }, ensure_ascii=False))
        await self.list_businesses()

    async def upgrade_business(self, business_id):
        success = await sync_to_async(self.player.upgrade_business)(business_id)
        await self.send(json.dumps({
            'action': 'upgrade',
            'business_id': business_id,
            'success': success
        }, ensure_ascii=False))
        await self.list_businesses()

    async def list_businesses(self):
        player_businesses = await sync_to_async(PlayerBusiness.objects.filter)(player=self.player)
        all_businesses = await sync_to_async(Business.objects.all)()

        player_businesses_list = await sync_to_async(list)(player_businesses)
        all_businesses_list = await sync_to_async(list)(all_businesses)

        context = {'request': self.scope}

        purchased_businesses_data = await sync_to_async(lambda: PlayerBusinessSerializer(player_businesses_list, many=True, context=context).data)()
        purchased_business_ids = [pb['business'] for pb in purchased_businesses_data]

        unpurchased_businesses = [b for b in all_businesses_list if b.id not in purchased_business_ids]
        unpurchased_businesses_data = await sync_to_async(lambda: BusinessSerializer(unpurchased_businesses, many=True, context=context).data)()

        await self.send(json.dumps({
            'action': 'list',
            'purchased_businesses': purchased_businesses_data,
            'unpurchased_businesses': unpurchased_businesses_data
        }, ensure_ascii=False))