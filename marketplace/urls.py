from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor-detail'),

    # cart functionality crud
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
]