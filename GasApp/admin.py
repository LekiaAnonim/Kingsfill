from django.contrib import admin

# Register your models here.
from .models import Batch, Sale
# Register your models here.


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    fields = ('batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name','vendor_phone', 'close_account')
    list_display = ('batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name','vendor_phone', 'close_account')
    list_filter = ('batch_name', 'date_created',)
    search_fields = ('batch_name', 'date_created',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ('batch','kg', 'price', 'date', 'customer_name', 'customer_phone')
    list_display = ('batch', 'kg', 'price', 'date', 'customer_name', 'customer_phone')
    list_filter = ('kg', 'price', 'date', 'customer_name', 'customer_phone')
    search_fields = ('kg', 'price', 'date', 'customer_name', 'customer_phone')
