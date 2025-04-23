from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('delete/', views.delete_products, name='delete_products'),
]