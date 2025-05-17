from django.contrib import admin
from .models import Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'store', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'store', 'created_at')
    search_fields = ('product__name', 'customer__email', 'store__name')
