from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from inventory.models import Product, StockMovement

@receiver(post_save, sender=Order)
def reduce_inventory_on_order(sender, instance, created, **kwargs):
    if created:  # only reduce stock on new orders
        product = instance.product
        product.stock_quantity -= instance.quantity
        product.save()

        # Optional: log stock movement
        StockMovement.objects.create(
            product=product,
            movement_type='OUT',
            quantity=instance.quantity
        )