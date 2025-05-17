from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order
from stores.models import Store
from django.db import models

# Create your views here.

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True, store__is_active=True)
    # فقط العملاء يمكنهم الطلب
    if request.user.user_type != 'customer':
        messages.error(request, 'فقط العملاء يمكنهم طلب المنتجات.')
        return redirect('products:product_detail', pk=product_id)
    # لا يمكن الطلب إذا الكمية غير متوفرة
    if product.quantity < 1:
        messages.error(request, 'المنتج غير متوفر حالياً.')
        return redirect('products:product_detail', pk=product_id)
    if request.method == 'POST':
        # يمكن لاحقاً دعم اختيار الكمية
        order = Order.objects.create(
            product=product,
            customer=request.user,
            store=product.store,
            quantity=1,
        )
        # تقليل الكمية من المنتج
        product.quantity -= 1
        product.save()
        messages.success(request, 'تم إنشاء الطلب بنجاح!')
        return redirect('orders:my_orders')
    return redirect('products:product_detail', pk=product_id)

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).select_related('product', 'store').order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def seller_orders(request):
    # التأكد أن المستخدم بائع وله متجر
    if request.user.user_type != 'seller' or not hasattr(request.user, 'store'):
        messages.error(request, 'هذه الصفحة مخصصة للبائعين فقط.')
        return redirect('/')
    store = request.user.store
    # تصفية الطلبات حسب الحقول
    status = request.GET.get('status')
    product_q = request.GET.get('product', '').strip()
    customer_q = request.GET.get('customer', '').strip()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    orders = Order.objects.filter(store=store).select_related('product', 'customer').order_by('-created_at')
    if status in dict(Order.STATUS_CHOICES):
        orders = orders.filter(status=status)
    if product_q:
        orders = orders.filter(product__name__icontains=product_q)
    if customer_q:
        orders = orders.filter(
            models.Q(customer__full_name__icontains=customer_q) |
            models.Q(customer__email__icontains=customer_q)
        )
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)
    return render(request, 'orders/seller_orders.html', {'orders': orders, 'current_status': status, 'status_choices': Order.STATUS_CHOICES})

@login_required
def order_detail_customer(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == 'POST' and order.status == 'pending' and 'cancel' in request.POST:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'تم إلغاء الطلب بنجاح.')
        return redirect('orders:order_detail_customer', order_id=order.id)
    return render(request, 'orders/order_detail_customer.html', {'order': order})
