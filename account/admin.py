from django.contrib import admin
from .models import Player, Business, PlayerBusiness

# Player Admin
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_id', 'profit', 'coin', 'level', 'referral_code', 'last_coin_update')
    search_fields = ('name', 'device_id', 'referral_code')
    list_filter = ('level', 'last_coin_update')
    ordering = ('-last_coin_update', 'name')

# Business Admin
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ranking', 'base_profit', 'cost', 'upgrade_cost_factor')
    search_fields = ('name',)
    list_filter = ('category', 'ranking')
    ordering = ('name',)

# PlayerBusiness Admin
class PlayerBusinessAdmin(admin.ModelAdmin):
    list_display = ('player', 'business', 'level', 'profit')
    search_fields = ('player__name', 'business__name')
    list_filter = ('business__category', 'level')
    ordering = ('-level', 'player')

# Register your models here if not using @admin.register
admin.site.register(Player, PlayerAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(PlayerBusiness, PlayerBusinessAdmin)
