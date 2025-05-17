from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from orders.models import Order
from stores.models import Store

def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})

@login_required
def seller_dashboard(request):
    if request.user.user_type != 'seller' or not hasattr(request.user, 'store'):
        messages.error(request, 'هذه الصفحة مخصصة للبائعين فقط.')
        return render(request, 'home.html')
    store = request.user.store
    products = Product.objects.filter(store=store)
    orders = Order.objects.filter(store=store)
    stats = {
        'products_count': products.count(),
        'orders_pending': orders.filter(status='pending').count(),
        'orders_delivered': orders.filter(status='delivered').count(),
        'products_unavailable': products.filter(quantity=0).count(),
        'low_stock_products': products.filter(quantity__gt=0, quantity__lte=5),
    }
    return render(request, 'dashboard.html', {'stats': stats, 'products': products, 'orders': orders, 'store': store}) 