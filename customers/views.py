from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.forms import UserInfoForm, UserProfileForm, UserProfile, User
from orders.models import Order
# Create your views here.

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



@login_required(login_url='loginUser')
@user_passes_test(check_role_customer)
def customer_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        user_form = UserInfoForm(request.POST,instance=request.user)
        if user_profile_form.is_valid() and user_form.is_valid():
            user_profile_form.save()
            user_form.save()
            messages.success(request, 'userprofile updated successfully')
            return redirect('c_profile')
        else:
            print(user_profile_form.errors)
            print(user_form.errors)



    else:
        user_profile_form = UserProfileForm(instance=user_profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': user_profile_form,
        'user_form': user_form,
        'profile': user_profile,
    }
    return render(request, 'customers/customer_profile.html', context)





def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'customers/my_orders.html', context)