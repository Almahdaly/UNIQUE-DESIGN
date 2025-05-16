from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('my-store/', views.setup_store, name='setup_store'),
] 