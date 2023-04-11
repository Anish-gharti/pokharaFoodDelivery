from django.shortcuts import render

# Create your views here.
def customer_profile(request):
    return render(request, 'customers/customer_profile.html')