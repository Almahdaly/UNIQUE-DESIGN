from django.db import models
from django.conf import settings
from products.models import Product
from stores.models import Store

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد التنفيذ'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"طلب {self.product.name} من {self.customer.full_name} ({self.get_status_display()})"
