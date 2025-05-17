from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from orders.models import Order
from stores.models import Store

# Create your views here.

@login_required
def add_to_cart(request, product_id):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'customer':
        messages.error(request, 'يجب أن تكون مسجلاً كمشتري لإضافة منتجات للسلة.')
        return redirect('products:product_detail', product_id=product_id)

    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    if quantity > product.quantity:
        quantity = product.quantity

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, 'تمت إضافة المنتج إلى السلة بنجاح.')
    return redirect('cart:view_cart')

@login_required
def view_cart(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'customer':
        messages.error(request, 'يجب أن تكون مسجلاً كمشتري لعرض السلة.')
        return redirect('home')
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    total = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST' and items:
        errors = []
        for item in items:
            product = item.product
            if item.quantity > product.quantity:
                errors.append(f"الكمية المطلوبة من {product.name} غير متوفرة.")
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'cart/view_cart.html', {'cart': cart, 'items': items, 'total': total})
        # إنشاء الطلبات وخصم الكمية
        for item in items:
            product = item.product
            Order.objects.create(
                product=product,
                customer=request.user,
                store=product.store,
                quantity=item.quantity,
            )
            product.quantity -= item.quantity
            product.save()
        # تفريغ السلة
        items.delete()
        messages.success(request, 'تم تأكيد الطلب وإرساله للبائع بنجاح!')
        return redirect('orders:my_orders')

    return render(request, 'cart/view_cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    item.update_quantity(quantity)
    messages.success(request, 'تم تحديث الكمية بنجاح.')
    return redirect('cart:view_cart')

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'تم حذف المنتج من السلة.')
    return redirect('cart:view_cart')
