from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import products,Cart,CartItem,User
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.conf import settings
from .models import Payment


def Register(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        username= request.POST.get('username')
        if form.is_valid():
            user=form.save()
            messages.success(request,f"newuser{username} created successfully")
            Cart.objects.create(user=user)
            return redirect('login')
        else:
            messages.error(request,"correct the errors below")
            return render (request,"register.html",{'form': form})
    return render (request,"register.html")

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            error_message= "incorrect username or password"
            return render (request,"login.html",{"error_message":error_message})
    return render (request,"login.html")

def Logout(request):
    logout(request)
    return redirect('login')


@login_required
def HomePage(request):
    return render (request,"homepage.html")

@login_required
def Products(request):
    Products = products.objects.all()
    paginator = Paginator(Products,4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    current_page = page_number if page_number else 1
    context =  {'products' : page_obj,'current_page' : current_page}
    return render (request,"products.html",context)

@login_required
def ProductDetails(request,id):
    product = products.objects.get(pk=id)
    context = {'product' : product}
    return render(request,'product_details.html',context)

@login_required
def cart(request):  
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items=cart.items.all()
    grand_total = sum(item.quantity * item.product.price for item in cart_items)
    tax = grand_total*10/100
    context={ 'cartitems' : cart_items,
              'subtotal' : grand_total,
              'tax' : tax,
              'grandtotal' : grand_total+tax
            }
    return render(request,'cart.html',context)

@login_required
def AddtoCart(request):
    if request.method == 'POST':
        user = request.user
        cart= Cart.objects.get(user= user)
        productid= request.POST.get('productid')
        product = products.objects.get(id= productid)
        quantity = request.POST.get('quantity')
       
        try:
            cart_item=CartItem.objects.get(cart=cart,product=product)
            cart_item.quantity+=int(quantity)
            cart_item.save()
        except ObjectDoesNotExist:
            cart_item=CartItem.objects.create(cart=cart ,product=product, quantity=quantity)
            cart_item.save()
        return redirect('cart')
    
@login_required
def RemoveCartItem(request,id):
    user = request.user
    cart = Cart.objects.get(user = user)
    cart_item = cart.items.get( id = id)
    cart_item.delete()
    return redirect('cart')

@login_required
def initiate_payment(request,amount):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount = float(amount)
    amount_in_paise = int(amount) * 100
    currency = "INR"

   
    razorpay_order = client.order.create({
        'amount': amount_in_paise,
        'currency': currency,
        'payment_capture': '1'
    })

   
    Payment.objects.create(
        user=request.user,
        order_id=razorpay_order['id'],
        amount=amount,
        status='CREATED'
    )

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount_in_paise,
        'currency': currency,
        'callback_url': '/paymenthandler/'
    }
    return render(request, 'checkout.html', context)