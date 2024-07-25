from django.contrib import admin
from .models import Cryptocurrency, Property, Stock, Vehicle

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

admin.site.register(Cryptocurrency, CryptocurrencyAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Vehicle, VehicleAdmin)