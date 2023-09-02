from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.db.models import Q
from .forms import SignupForm
from product.models import Product,Category

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form= SignupForm(request.POST)

        if form.is_valid():
            user= form.save()

            login(request,user)
            return redirect('/')
        
    else:
        form= SignupForm()
    context={'form':form}   
    return render(request,'core/signup.html',context)

@login_required
def myaccount(request):
    return render(request,'core/myaccount.html')

@login_required
def edit_myaccount(request):

    if request.method == 'POST':
        print('post')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        
        user= request.user
        user.first_name= first_name
        user.last_name= last_name
        user.email= email
        user.username= username
        user.save()
        return redirect('core:myaccount')
    else:
        print('not post')

    return render(request,'core/edit_myaccount.html')

def home(request):
    products= Product.objects.all()[0:8]
    context={'products':products}
    return render(request,'core/home.html',context)

def shop(request):
    categories = Category.objects.all()
    products= Product.objects.all()

    active_category = request.GET.get('category','')

    if active_category:
        products= products.filter(category__slug=active_category)

    query = request.GET.get('query','')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context={'products':products,
             'categories':categories,
             'active_category':active_category}
    return render(request,'core/shop.html',context)
