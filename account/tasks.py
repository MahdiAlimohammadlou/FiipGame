from celery import shared_task
from django.utils import timezone
from .models import Player
from decimal import Decimal, ROUND_DOWN

@shared_task
def update_player_coins():
    players = Player.objects.all()
    current_time = timezone.now()

    for player in players:
        time_difference_seconds = (current_time - player.last_coin_update).total_seconds()
        time_difference_hours = Decimal(time_difference_seconds / 3600).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        profit_to_add = player.profit * time_difference_hours
        
        player.coin += profit_to_add.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        player.last_coin_update = current_time
        print("coins : ", player.coin)
        player.save()