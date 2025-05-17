from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart({self.user})"

    def total(self):
        return sum(item.subtotal() for item in self.items.select_related('product'))

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity

    def update_quantity(self, quantity):
        if quantity < 1:
            self.delete()
        else:
            self.quantity = quantity
            self.save()
