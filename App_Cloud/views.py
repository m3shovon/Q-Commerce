from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Restaurant, FoodItem, MyUser, Table, BookingRecord, FoodOrder,RestaurantCategories
from django.db.models import Q

# Create your views here.

def index(request):
    rests = Restaurant.objects.all()
    cats = RestaurantCategories.objects.all()
    context = {
        "rests" : rests,
        "cats" : cats
    }
    return render(request,"App_Cloud/index.html",context)


def help(request):
    return redirect(f"https://wa.me/+8801521430255?text=Need Some Help?")

def register(request):
    # form = NewUserForm()
    return render(request,"register.html")

def login_user(request):
    if request.method == "POST":
        user = request.POST.get("user")
        password = request.POST.get("password")
        userr = authenticate(request,username=user,password=password)
        if userr is not None:
            login(request,userr)
            return redirect("App_Cloud:viewprofile")
        else:
            messages.success(request, 'Your username or password is wrong!')
            return redirect("App_Cloud:register")       
    # return render(request,"user/index.html")

def logout_user(request):
    logout(request)
    return redirect("App_Cloud:register")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        photo = request.FILES.get("photo")
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            usr = User.objects.create_user(username=username, password=password1,email=email)
            usr.save()
            obj = MyUser.objects.create(user=usr,address=address,photo=photo,phone=phone)
            obj.save()
            user = authenticate(request,username=username,password=password1)    
            login(request,user)
        else:
            messages.success(request, 'Password not similar')
            return redirect("App_Cloud:register")     
        return redirect("/register")
    
@login_required(login_url='/register')   
def viewprofile(request):
    usr = User.objects.get(id=request.user.id)
    objects = BookingRecord.objects.filter(user=usr)
    orders = FoodOrder.objects.filter(user=usr)
    context = {
        "objects" : objects,
        "orders" : orders
    }
    
    return render(request,"viewprofiel.html",context)
def search(request):
    query = request.GET.get("search")
    if query != "":
        rests = Restaurant.objects.filter(
        Q(name__icontains=query) | Q(location__icontains=query) 
    )
                        
    else:
        rests = Restaurant.objects.all()
    
    context ={
        "rests" : rests
    }
    return render(request,"result.html",context)
def catsearch(request):
    query = request.GET.get("search")
    cat = RestaurantCategories.objects.get(id=query)
    rests = Restaurant.objects.filter(category=cat)
    
    context ={
        "rests" : rests
    }
    return render(request,"result.html",context)
def searchfood(request):
    query = request.GET.get("search")
    if query != "":
        items = FoodItem.objects.filter(
        Q(title__icontains=query) | Q(price__icontains=query) 
    )
                        
    else:
        items = FoodItem.objects.all()
    
    context ={
        "items" : items
    }
    return render(request,"App_Cloud/foodresult.html",context)

def visitresturants(request,id):
    rest = Restaurant.objects.get(id=id)
    tables = Table.objects.filter(restaurant=rest)
    total_tables = tables.count()
    seats = 0
    for t in tables:
        seats = seats + t.seats
    items = FoodItem.objects.filter(restaurant=rest)
    context = {
        "items" : items,
        "rest" : rest,
        "total_tables" : total_tables,
        "seats" : seats
    }
    return render(request,"App_Cloud/visitresturants.html",context)

def tables(request,id):
    rest = Restaurant.objects.get(id=id)
    tables = Table.objects.filter(restaurant=rest)
    context = {
        "rest" : rest,
        "tables" : tables
    }
    return render(request,"App_Cloud/tables.html",context)


def booknow(request,res,tb):
    tab = Table.objects.get(restaurant=res,id=tb)
    tab.booking_status = True
    tab.save()
    rest = Restaurant.objects.get(id=res)
    tabl = Table.objects.get(id=tb)
    us = User.objects.get(id=request.user.id)
    obj = BookingRecord.objects.create(user=us,restaurant=rest,table=tabl)
    obj.save()
    return redirect("App_Cloud:viewprofile")

def orderfood(request,id):
    item = FoodItem.objects.get(id=id)
    us = User.objects.get(id=request.user.id)
    obj = FoodOrder.objects.create(item=item,user=us,bill=item.price)
    obj.save()
    return redirect("App_Cloud:viewprofile")
