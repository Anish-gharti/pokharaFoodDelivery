from django.urls import path
from accounts import views as AccountViews
from . import views
urlpatterns = [
  path('', AccountViews.custDashboard, name='customer'),
  path('profile/', views.customer_profile, name='c_profile'),
  path('my-orders/', views.my_orders, name='customer_my_orders'),
  path('order-detail/<int:order_number>/', views.order_detail, name='order-detail'),
]