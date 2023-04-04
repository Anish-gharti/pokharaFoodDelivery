from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
]


# AIzaSyDJFH5sYAeK9gEP_D0uMrihHA0t3jVlV6k


#