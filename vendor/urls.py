from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menuBuilder, name='menu-builder'),

    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # category crud
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit-category/<int:pk>/', views.edit_category, name='edit-category'),
    path('menu-builder/category/delete_catgeory/<int:pk>/', views.delete_category, name='delete_category'),

    # fooditem crud
    path('menu-builder/food/add/', views.add_food, name='add-food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit-food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete-food'),

    # opening hours
    path('opening-hours/', views.opening_hours, name='opening-hours'),
    path('opening-hours/add/', views.add_opening_hour, name='add_opening_hours'),

]


