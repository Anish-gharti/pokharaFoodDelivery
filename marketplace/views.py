from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved =True)
    v_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': v_count,
    }
    return render(request, 'marketplace/listings.html', context)




def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems',
                 queryset=FoodItem.objects.filter(is_available=True))
    )

      
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
        except:
            cart_items = None    
    cart_items = None        
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the fooditem exits:
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the food item is already added or not
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase the cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status': 'success', 'message': 'increased the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity,})
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'food item added to cart successfully.', 'cart_counter':get_cart_counter(request),'qty':check_cart.quantity,})
            except:
                return JsonResponse({'status': 'failed', 'message': 'this food doesnot exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'invalid request'})
    
    

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})     
    

def decrease_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the fooditem exits:
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the food item is already added or not
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # decrease the cart quantity
                    if check_cart.quantity >1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0

                    return JsonResponse({'status': 'success', 'message': 'decreased the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity,})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'You donot have item in the cart.'})
            except:
                return JsonResponse({'status': 'failed', 'message': 'this food doesnot exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'invalid request'})
    
    

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})     
    

def cart(request):
    return render(request, 'marketplace/cart.html')    