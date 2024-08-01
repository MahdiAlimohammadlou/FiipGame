from django.contrib import admin
from .models import Player, PlayerBusiness, Avatar

# Player Admin
class AvatarAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'gender')
    search_fields = ( 'name',)
    list_filter = ('gender',)
    ordering = ('name', )

# Player Admin
class PlayerAdmin(admin.ModelAdmin):
    list_display = ( 'profit', 'coin', 'level', 'referral_code', 'last_coin_update')
    search_fields = ( 'referral_code',)
    list_filter = ('level', 'last_coin_update')
    ordering = ('-last_coin_update', )

# PlayerBusiness Admin
class PlayerBusinessAdmin(admin.ModelAdmin):
    list_display = ('player', 'business', 'level', 'profit')
    search_fields = ('business__name',)
    list_filter = ('business__category', 'level')
    ordering = ('-level', 'player')

# Register your models here if not using @admin.register
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerBusiness, PlayerBusinessAdmin)
admin.site.register(Avatar, AvatarAdmin)
