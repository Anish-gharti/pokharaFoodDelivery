
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from marketplace.models import Cart, Tax
from marketplace.context_processors import get_cart_amount
from menu.models import FoodItem
from .forms import OrderForm
from .models import Order, OrderedFood, Payment
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
import simplejson as json
from . utils import generate_order_number

# Create your views here.
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amount(request)['sub_total']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # phone = form.cleaned_data['phone']
            # email = form.cleaned_data['email']
            # address = form.cleaned_data['address']
            # country = form.cleaned_data['country']
            # state = form.cleaned_data['state']
            # city = form.cleaned_data['city']
            # pin_code = form.cleaned_data['pin_code']
            
            # order = Order(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address, country=country, state=state,
            #               city=city, pin_code=pin_code)
            # order = form.save(commit=False)
            # order.user = request.user
            # order.total = grand_total
            # order.tax_data = json.dumps(tax_data)
            # order.total_tax = total_tax
            # order.payment_method = request.POST['payment_method']
            # order.order_number = "123"
            # order.save()
            # return redirect('place-order')
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            return redirect('place-order')
        else:
            print(form.errors)    
    return render(request, 'orders/place_order.html')