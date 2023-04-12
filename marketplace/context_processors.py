from .models import Cart, Tax
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0                

    return  dict(cart_count=cart_count)


def get_cart_amount(request):
    tax = 0
    sub_total = 0
    grand_total =0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            for cart_item in cart_items:
                fooditem = FoodItem.objects.get(pk=cart_item.fooditem.id)
                sub_total += (fooditem.price * cart_item.quantity)

        get_tax = Tax.objects.filter(is_active=True)

        for tax_types in get_tax:   
            tax_type =tax_types.tax_type
            tax_percentage = tax_types.tax_percentage
            tax_amount = round((tax_percentage * sub_total)/100, 2)
            tax_dict.update({tax_type:{str(tax_percentage): tax_amount}})
        for key in tax_dict.values():
            for x in key.values():
            
                tax = tax + x
        
        # tax = sum(x for key in tax_dict.values() for x in key.values())
        # print("tax", tax)
        grand_total  += sub_total + tax
    return dict(sub_total=sub_total, grand_total=grand_total, tax_dict=tax_dict, tax=tax)            