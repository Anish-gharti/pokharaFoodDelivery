from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amount
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_customer
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import  Distance
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
                    return JsonResponse({'status': 'success', 'message': 'increased the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'food item added to cart successfully.', 'cart_counter':get_cart_counter(request),'qty':check_cart.quantity,'cart_amount': get_cart_amount(request)})
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

                    return JsonResponse({'status': 'success', 'message': 'decreased the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'You donot have item in the cart.'})
            except:
                return JsonResponse({'status': 'failed', 'message': 'this food doesnot exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'invalid request'})
    
    

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})     
    
@login_required(login_url='loginUser')
@user_passes_test(check_role_customer)
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)    


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id) 
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'cartitem is successfully deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'cart item doesnot exist'})    
                
        else:
            return JsonResponse({'status': 'failed', 'message': 'invalid request'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'please login to continue'})
  
        
def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address= request.GET['address']
        latitude= request.GET['lat']

        longitude= request.GET['lng']

        radius= request.GET['radius']
        rest_name = request.GET['rest_name']

        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_item__icontains=rest_name, is_available=True).values_list('vendor', flat=True)
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(is_approved=True, user__is_active=True,vendor_name__icontains=rest_name))

        if  latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
            print(pnt)
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(is_approved=True, user__is_active=True,vendor_name__icontains=rest_name) 
                                            ,user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km)

        v_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': v_count,
            'source_location': address,
        }
        return render(request, 'marketplace/listings.html', context)        