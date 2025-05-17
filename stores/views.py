from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store
from .forms import StoreForm
from django.db.models import Q

@login_required
def setup_store(request):
    try:
        store = Store.objects.get(user=request.user)
        is_new = False
    except Store.DoesNotExist:
        store = None
        is_new = True

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store_obj = form.save(commit=False)
            store_obj.user = request.user
            store_obj.save()
            messages.success(request, 'تم حفظ بيانات المتجر بنجاح.')
            return redirect('stores:setup_store')
    else:
        form = StoreForm(instance=store)

    return render(request, 'stores/store_setup.html', {
        'form': form,
        'store': store,
        'is_new': is_new,
    })

def public_store(request, slug):
    store = Store.objects.filter(slug=slug, is_active=True).first()
    if not store:
        return render(request, '404.html', status=404)
    products = store.products.all()
    # فلاتر البحث
    name_q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    price_min = request.GET.get('price_min', '').strip()
    price_max = request.GET.get('price_max', '').strip()
    available = request.GET.get('available')
    if name_q:
        products = products.filter(name__icontains=name_q)
    if category:
        products = products.filter(category__icontains=category)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if available == '1':
        products = products.filter(is_available=True, quantity__gt=0)
    # جلب التصنيفات الفريدة
    categories = store.products.values_list('category', flat=True).distinct()
    return render(request, 'stores/public_store.html', {
        'store': store,
        'products': products,
        'categories': categories,
        'filters': {
            'q': name_q,
            'category': category,
            'price_min': price_min,
            'price_max': price_max,
            'available': available,
        }
    })

# Create your views here.
