from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('vendor/', include('vendor.urls')),
    path('customers/', include('customers.urls')),


]