
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
from .utils import generate_order_number

# Create your views here.
@login_required(login_url='loginUser')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')

    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    # subtotal = get_cart_amount(request)['sub_total']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
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
            context = {
                'order': order,
                'cart_items': cart_items,
                'anish': 'anish'
            }
        
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)    
              
    return render(request, 'orders/place_order.html')

@login_required(login_url='loginUser')
def payments(request):
         # Check if the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()
     
        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()
        

        # move the cart items to the ordered food model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity
            ordered_food.save()

        # send email to the customer after the order is completed
        mail_subject = 'Thank you for ordering food with us.'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,

        }
        send_notification(mail_subject, mail_template, context) 


        # send email to the vendors
        mail_subject = 'you have received a new order'
        mail_template ='orders/new_order_received.html'
        to_emails = []
        for num_of_emails in cart_items:
            if num_of_emails.fooditem.vendor.user.email not in to_emails:
                to_emails.append(num_of_emails.fooditem.vendor.user.email)
        print(to_emails)        
        context = {
            'order': order,
            'to_email': to_emails,
        }
        send_notification(mail_subject, mail_template, context)

        # delete cartitems
        cart_items.delete()
    else:
        print("aaaaaaaaaaaaaaa")
