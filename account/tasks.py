# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Player

@shared_task
def update_player_coins():
    players = Player.objects.all()
    for player in players:
        hours_since_last_update = (timezone.now() - player.updated_at).total_seconds() 
        if hours_since_last_update > 0:
            player.coin += int(player.profit * hours_since_last_update)
            player.save()
