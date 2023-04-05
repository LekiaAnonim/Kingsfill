from django.contrib import admin

# Register your models here.
from .models import Batch, Sale, Shop
# Register your models here.

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    fields = ('user','shop_name', 'location', 'shop_manager', 'manager_phone', 'date_created')
    list_display = ('shop_name', 'location', 'shop_manager', 'manager_phone', 'date_created')
    list_filter = ('shop_name', 'date_created',)
    search_fields = ('shop_name', 'date_created',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    fields = ('shop','batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name','vendor_phone', 'close_account')
    list_display = ('batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name','vendor_phone', 'close_account')
    list_filter = ('batch_name', 'date_created',)
    search_fields = ('batch_name', 'date_created',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ('batch','kg', 'price', 'date', 'customer_name', 'customer_phone')
    list_display = ('batch', 'kg', 'price', 'date', 'customer_name', 'customer_phone')
    list_filter = ('kg', 'price', 'date', 'customer_name', 'customer_phone')
    search_fields = ('kg', 'price', 'date', 'customer_name', 'customer_phone')
