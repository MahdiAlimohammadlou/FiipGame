from django.contrib import admin
from .models import Player, Business, PlayerBusiness

# Register your models here.
admin.site.register(Player)
admin.site.register(Business)
admin.site.register(PlayerBusiness)