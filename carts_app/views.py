from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from store_app.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
# Create your views here.

# put product without login also in card sections
# for card.html
def _card_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# add perticular item to card 
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  #get the product
    product_variation = []
    if request.method == 'POST':
        # for geting size and color of product from url
        for item in request.POST:
            key = item 
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                # ------
                product_variation.append(variation)
            except:
                pass
        # size = request.GET['size']
        
    
    try:
        cart = Cart.objects.get(cart_id=_card_id(request)) #get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _card_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # --------variation card select 
        if len(product_variation) > 0:
            cart_item.variations.clear() #each time new color and size will be taken
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.quantity += 1  # cart_item.quantitity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )  
        # --------variation card select 
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()
    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')

# decrement items
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _card_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# remove holl card pertucuar
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _card_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')







def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax


    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    } 
    return render(request, 'store/cart.html', context)




# creating checkout page 
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax


    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    } 
    return render(request, 'store/checkout.html', context)