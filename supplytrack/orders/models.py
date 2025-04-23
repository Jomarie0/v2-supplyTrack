from django.db import models
from inventory.models import Product
import string, random

def generate_unique_order_id():
    while True:
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id

class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False, default=generate_unique_order_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Canceled", "Canceled")],
        default="Pending"
    )

    def __str__(self):
        return f"{self.order_id} - {self.product.name}"
