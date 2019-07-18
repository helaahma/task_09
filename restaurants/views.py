from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout,  authenticate
from .models import Restaurant
from .forms import RestaurantForm, SignUpForm, Signin

def signup(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid:
            user= form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login (request,user)
            return redirect("restaurant-list")
    context= {
    "form": form,
    }

    return render(request, 'signup.html', context)
    message=""
def signin(request):
    form= Signin()
    if request.method=='POST':
        form=Signin (request.POST)
        if form.is_valid():
            user_name= form.cleaned_data['user_name']
            password=form.cleaned_data['password']
            authentication= authenticate(username=user_name, password=password)
            if authentication is not None:
                login(request, authentication)
                return redirect('restaurant-list')
            else:
                message= "Re-enter password"
    context={
    "form":form,
    "m": message,
    }

    
    return render(request, 'signin.html', context)

def signout(request):
    logout (request)
    return redirect(request, 'signin.html', context)

def restaurant_list(request):
    context = {
        "restaurants":Restaurant.objects.all()
    }
    return render(request, 'list.html', context)


def restaurant_detail(request, restaurant_id):
    context = {
        "restaurant": Restaurant.objects.get(id=restaurant_id)
    }
    return render(request, 'detail.html', context)

def restaurant_create(request):
    form = RestaurantForm()
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def restaurant_update(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    form = RestaurantForm(instance=restaurant_obj)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant_obj)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "restaurant_obj": restaurant_obj,
        "form":form,
    }
    return render(request, 'update.html', context)

def restaurant_delete(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    restaurant_obj.delete()
    return redirect('restaurant-list')
