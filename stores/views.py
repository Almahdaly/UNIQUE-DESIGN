from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store
from .forms import StoreForm

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
    # جلب المنتجات الفعلية المرتبطة بالمتجر
    products = store.products.all()
    return render(request, 'stores/public_store.html', {
        'store': store,
        'products': products,
    })

# Create your views here.
