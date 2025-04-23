from django.contrib import admin
from .models import Product, PurchaseOrder, StockMovement

admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(StockMovement)
