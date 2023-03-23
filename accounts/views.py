from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib import messages
from .models import User
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
            messages.success(request, f'account is created for {username} successfully.')

            return redirect('home')
        else:
            print(form.errors)
            
    else:    
        form = UserForm()
    conntext = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', conntext)