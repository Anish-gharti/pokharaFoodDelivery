from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm, Vendor
from accounts.forms import UserProfileForm, UserProfile
from django.contrib import messages
from accounts.views import check_role_vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import get_vendor
from django.template.defaultfilters import slugify
from menu.models import Category, FoodItem

from menu.forms import CategoryForm
# Create your views here.

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "profile settings for vendor updated.")
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:

        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }

    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, id=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)

    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)



def add_category(request):
    vendor = get_vendor(request)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "category added successfully")
            return redirect('menu-builder')
        else:
            print(form.errors)    
            return redirect('add_category') 
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }        
    return render(request, 'vendor/add_category.html', context)