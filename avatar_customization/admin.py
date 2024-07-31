from django.contrib import admin
from .models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category_type', 'price',
    )
    search_fields = ('name', 'category_type')
    list_filter = ('category_type',)
    ordering = ('name',)

admin.site.register(Item, ItemAdmin)
