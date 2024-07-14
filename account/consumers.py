from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Business, PlayerBusiness

class BusinessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.player = self.scope.get('user', None)

        if self.player is None or self.player.is_anonymous:
            await self.accept()
            await self.send_error("Invalid API key.")
            await self.close()
            return

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
        business = await database_sync_to_async(Business.objects.get)(id=business_id)
        success = await database_sync_to_async(self.player.buy_business)(business)
        await self.send(json.dumps({
            'action': 'buy',
            'business_id': business_id,
            'success': success
        }, ensure_ascii=False))
        await self.list_businesses()

    async def upgrade_business(self, business_id):
        success = await database_sync_to_async(self.player.upgrade_business)(business_id)
        await self.send(json.dumps({
            'action': 'upgrade',
            'business_id': business_id,
            'success': success
        }, ensure_ascii=False))
        await self.list_businesses()

    async def list_businesses(self):
        player_businesses = await database_sync_to_async(PlayerBusiness.objects.filter)(player=self.player)
        all_businesses = await database_sync_to_async(Business.objects.all)()

        player_businesses_list = await database_sync_to_async(list)(player_businesses)
        all_businesses_list = await database_sync_to_async(list)(all_businesses)

        purchased_businesses_data = [
            {
                'id': await database_sync_to_async(lambda pb: pb.business.id)(pb),
                'name': await database_sync_to_async(lambda pb: pb.business.name)(pb),
                'level': pb.level,
                'profit': str(pb.profit),
                'upgrade_cost': str(pb.upgrade_cost),
                'category': pb.business.category,
                'ranking': pb.business.ranking
            }
            for pb in player_businesses_list
        ]

        purchased_business_ids = [pb['id'] for pb in purchased_businesses_data]
        unpurchased_businesses = [b for b in all_businesses_list if b.id not in purchased_business_ids]

        unpurchased_businesses_data = [
            {
                'id': b.id,
                'name': b.name,
                'cost': str(b.cost),
                'base_profit': str(b.base_profit),
                'category': b.category,
                'ranking': b.ranking
            }
            for b in unpurchased_businesses
        ]

        await self.send(json.dumps({
            'action': 'list',
            'purchased_businesses': purchased_businesses_data,
            'unpurchased_businesses': unpurchased_businesses_data
        }, ensure_ascii=False))