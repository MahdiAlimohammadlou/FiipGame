from django.contrib import admin
from .models import Business, Cryptocurrency, Property, Stock, Vehicle

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ranking', 'base_profit', 'cost', 'upgrade_cost_factor')
    search_fields = ('name',)
    list_filter = ('category', 'ranking')
    ordering = ('name',)

class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'purchasable_quantity', 'currency_logo')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('name',)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'property_img')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('name',)

class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'purchasable_quantity', 'stock_logo')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('name',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'vehicle_type', 'vehicle_img')
    search_fields = ('name', 'vehicle_type')
    list_filter = ('vehicle_type', 'price')
    ordering = ('name',)

admin.site.register(Business, BusinessAdmin)
admin.site.register(Cryptocurrency, CryptocurrencyAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Vehicle, VehicleAdmin)