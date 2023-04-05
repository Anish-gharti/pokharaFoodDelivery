from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menuBuilder, name='menu-builder'),

    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
]


