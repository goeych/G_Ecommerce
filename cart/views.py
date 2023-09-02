from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .cart import Cart
from product.models import Product

# Create your views here.

def add_to_cart(request,product_id):
    cart= Cart(request)
    cart.add(product_id)
    return render(request,'cart/partials/menu_cart.html')

def cart(request):
    cart= Cart(request)

    print(cart)
    for item in cart:
        print(item)
    return render(request,'cart/cart.html')

def success(request):
    return render(request,'cart/success.html')

def update_cart(request,product_id,action):
    cart= Cart(request)

    if action == 'increment':
        cart.add(product_id,1,True)
    else:
        cart.add(product_id,-1,True)
    
    product= Product.objects.get(pk=product_id)
    quantity= cart.get_item(product_id)

    if quantity:
        quantity= quantity['quantity']

        item= {
            'product':{
                'id':product.id,
                'name':product.name,
                'image':product.image,
                'get_thumbnail':product.get_thumbnail(),
                'price':product.price,
            },
            'total_price':(quantity * product.price) / 100,
            'quantity':quantity,
        }
    else:
        item= None
        
    context={'item':item}

    response= render(request,'cart/partials/cart_item.html',context)
    response['HX-Trigger']= 'update-menu-cart'
    return response

@login_required
def checkout(request):
    pub_key= settings.STRIPE_API_KEY_PUBLISHABLE
    context={'pub_key':pub_key}
    return render(request,'cart/checkout.html',context)

def hx_menu_cart(request):
    return render(request,'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request,'cart/partials/cart_total.html')