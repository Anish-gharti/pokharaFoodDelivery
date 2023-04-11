from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.forms import UserInfoForm, UserProfileForm, UserProfile, User
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

    user_profile_form = UserProfileForm(instance=user_profile)
    user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': user_profile_form,
        'user_form': user_form,
    }
    return render(request, 'customers/customer_profile.html', context)