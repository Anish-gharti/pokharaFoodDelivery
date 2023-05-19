
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib import messages
from .models import User,UserProfile
from vendor.models import Vendor
from vendor.forms import VendorForm
from django.contrib import auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from orders.models import Order
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
            # send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
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
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+ '-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
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

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active  = True
        user.save()
        messages.success(request, "congratulations, your account is activated.")
        return redirect('loginUser')
    else:
        messages.error(request, "invalid activation link")  
        return redirect('myAccount')  


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
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'recent_orders': recent_orders,
       
        'orders_count': orders.count(),
    }
    return render(request, 'accounts/custDashboard.html', context)


@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor =Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')

    context = {
        'orders':orders,
        'orders_count': orders.count()
    }
    return render(request, 'accounts/vendorDashboard.html', context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, f'password reset link has been sent to {user.first_name} email address.')
            return redirect('loginUser')
        
        else:
            messages.error(request, 'account doesnot exist.')
            return redirect('forgotPassword')
        
    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')



def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['password']

        if password == confirm_password:
            pk =request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "your password iss successfully changed")
    return render(request, 'accounts/resetPassword.html')