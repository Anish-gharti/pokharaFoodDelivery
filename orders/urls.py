from django.urls import path
from .import views

urlpatterns = [
    path('place-order/', views.place_order, name='place-order'),
    path('payments/', views.payments, name='payments'),
    path('order-complete/', views.order_complete, name='order-complete'),
]