from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('my/', views.my_orders, name='my_orders'),
    path('store-orders/', views.seller_orders, name='seller_orders'),
    path('my/<int:order_id>/', views.order_detail_customer, name='order_detail_customer'),
    # سيتم إضافة مسارات أخرى لاحقاً
] 