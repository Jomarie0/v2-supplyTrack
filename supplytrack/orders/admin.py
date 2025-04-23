from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product', 'quantity', 'order_date', 'expected_delivery', 'status')
    search_fields = ('order_id', 'product__name')
    list_filter = ('status',)
    ordering = ('-order_date',)
