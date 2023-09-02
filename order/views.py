import json
import stripe
from django.http import JsonResponse
from django.conf import settings
from cart.cart import Cart
from .models import Order,OrderItem
# Create your views here.
def start_order(request):
    cart= Cart(request)

    data= json.loads(request.body)
    total_price= 0
    items= []

    for item in cart:
        
        product= item['product']
        total_price += product.price * int(item['quantity'])
       

        obj= {
            'price_data':{
                'currency':'usd',
                'product_data':{
                    'name':product.name,
                },
                'unit_amount':product.price,
            },
            'quantity':item['quantity']
        }
        items.append(obj)


    stripe.api_key= settings.STRIPE_API_KEY_HIDDEN
    session= stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success/',
        cancel_url='http://127.0.0.1:8000/cart/'
    )

    payment_intent= session.payment_intent

    # first_name= data['first_name']
    # last_name= data['last_name']
    # email= data['email']
    # address= data['address']
    # zipcode= data['zipcode']
    # place= data['place']
    # phone= data['phone']

    # first_name= data.get('first_name')
    # last_name= data.get('last_name')
    # email= data.get('email')
    # address= data.get('address')
    # zipcode= data.get('zipcode')
    # place= data.get('place')
    # phone= data.get('phone')
    
    order= Order.objects.create(user=request.user,
                                first_name=data['first_name'],
                                last_name=data['last_name'],
                                email=data['email'],
                                address=data['address'],
                                place=data['place'],
                                phone=data['phone'],
                                zipcode=data['zipcode'],
                                #payment_intent= payment_intent,
                                paid_amount= total_price,
                                paid= True
                                )
    order.payment_intent= payment_intent
    # order.paid_amount= total_price
    # order.paid= True
    order.save()

# disable on part17
    # if request.method== 'POST':
    #     first_name= request.POST.get('first_name')
    #     last_name= request.POST.get('last_name')
    #     email= request.POST.get('email')
    #     address= request.POST.get('address')
    #     zipcode= request.POST.get('zipcode')
    #     place= request.POST.get('place')
    #     phone= request.POST.get('phone')
        
    #     order= Order.objects.create(user=request.user,
    #                                 first_name=first_name,
    #                                 last_name=last_name,
    #                                 email=email,
    #                                 address=address,
    #                                 place=place,
    #                                 phone=phone,
    #                                 zipcode=zipcode
    #                                 )
        
    for item in cart:
        product= item['product']
        quantity= int(item['quantity'])
        price= product.price * quantity
        item= OrderItem.objects.create(order=order,
                                       product=product,
                                       price=price,
                                       quantity=quantity)
 
    #clear cart session
    cart.clear()
    #     return redirect('core:myaccount')
    # return redirect('cart:cart')
    return JsonResponse({'session':session,'order':payment_intent})
