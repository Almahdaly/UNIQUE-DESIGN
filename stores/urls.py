from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('my-store/', views.setup_store, name='setup_store'),
    path('<slug:slug>/', views.public_store, name='public_store'),
] 