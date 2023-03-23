
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib import messages
from .models import User,UserProfile
from vendor.models import Vendor
from vendor.forms import VendorForm
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

# restricting the vendors from accesting the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    

# restricting the customer from accesting the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied




def registerUser(request):
    if request.user.is_authenticated:
        messages.info(request, "you are logged in already")
        return redirect('myAccount')
    elif request.method == "POST":
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
    if request.user.is_authenticated:
        messages.warning(request, "you are logged in already")
        return redirect('myAccount')
    elif request.method == "POST":
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


def loginUser(request):
    if request.user.is_authenticated:
        messages.info(request, "you are logged in already")
        return redirect('myAccount')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "you are logged in successfully")
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid credintials')
            return redirect('loginUser')    
    return render(request, 'accounts/login.html')


def logoutUser(request):
    auth.logout(request)
    messages.info(request, "you are logged out successfully.Please return soon")
    return redirect('loginUser')



@login_required(login_url='loginUser')
def myAccount(request):
    user = request.user
    redirectUrl =detectUser(user)

    return redirect(redirectUrl)

@login_required(login_url='loginUser')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')