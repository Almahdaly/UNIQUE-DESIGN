from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from stores.models import Store

# Create your views here.

@login_required
def my_products(request):
    store = getattr(request.user, 'store', None)
    if not store:
        messages.error(request, 'يجب عليك إعداد متجرك أولاً.')
        return redirect('stores:setup_store')
    products = Product.objects.filter(store=store)

    # تحديد وضع التعديل أو الحذف
    edit_pk = request.GET.get('edit')
    delete_pk = request.GET.get('delete')
    edit_mode = False
    form = None

    # حذف المنتج
    if delete_pk:
        product = get_object_or_404(Product, pk=delete_pk, store=store)
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'تم حذف المنتج بنجاح.')
            return redirect('products:my_products')
        # تأكيد الحذف عبر نافذة JS فقط

    # تعديل المنتج
    elif edit_pk:
        product = get_object_or_404(Product, pk=edit_pk, store=store)
        edit_mode = True
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'تم تعديل المنتج بنجاح.')
                return redirect('products:my_products')
        else:
            form = ProductForm(instance=product)

    # إضافة منتج جديد
    else:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.store = store
                product.save()
                messages.success(request, 'تم إضافة المنتج بنجاح.')
                return redirect('products:my_products')
        else:
            form = ProductForm()

    return render(request, 'products/my_products.html', {
        'products': products,
        'form': form,
        'edit_mode': edit_mode,
    })

@login_required
def add_product(request):
    store = getattr(request.user, 'store', None)
    if not store:
        messages.error(request, 'يجب عليك إعداد متجرك أولاً.')
        return redirect('stores:setup_store')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, 'تم إضافة المنتج بنجاح.')
            return redirect('products:my_products')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    store = getattr(request.user, 'store', None)
    product = get_object_or_404(Product, pk=pk, store=store)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المنتج بنجاح.')
            return redirect('products:my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    store = getattr(request.user, 'store', None)
    product = get_object_or_404(Product, pk=pk, store=store)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'تم حذف المنتج بنجاح.')
        return redirect('products:my_products')
    return render(request, 'products/delete_product.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, store__is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})
