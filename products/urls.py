from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('my/', views.my_products, name='my_products'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
] 