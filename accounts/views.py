from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib import messages
from .models import User,UserProfile
from vendor.models import Vendor
from vendor.forms import VendorForm
# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
        #    creatin the user using the form
        #    user = form.save(commit=False)
        #    password = form.cleaned_data['password']
        #    print(password)
        #    user.role = user.CUSTOMER
        #    user.set_password(password)
        #    user.save()

        # create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = user.CUSTOMER
            user.save()
            messages.success(request, f'account with username {username} is created successfully.')

            return redirect('registerUser')
        else:
            messages.error(request, 'invalid credintials')
            return redirect('registerUser')
            
    else:    
        form = UserForm()
    conntext = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', conntext)


def registerVendor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = user.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'your account has been registered succesfully')
            return redirect('registerVendor')
        else:
            print(form.errors)

    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }             
    return render(request, 'accounts/registerVendor.html',context)