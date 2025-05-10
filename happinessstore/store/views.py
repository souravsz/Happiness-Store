from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import products

def Register(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        username= request.POST.get('username')
        if form.is_valid():
            form.save()
            messages.success(request,f"newuser{username} created successfully")
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

def Products(request):
    Products = products.objects.all()
    context =  {'products' : Products}
    return render (request,"products.html",context)


