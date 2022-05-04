from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
#Edit Profile Imports
from django.contrib.auth.forms import UserChangeForm

import stripe

stripe.api_key = "sk_test_51KkfWMKqLUf6DKofStjiqe6J8BkSF02Ggcocp90zWsk25OnlT27JVeuuKzfhizPNK1oOyWvQXRMvMeEkG8ERVVk900RXLXnfjZ"

def checkout(request):
	if request.method == 'POST':

		print('Data:', request.POST)

		amount = float(request.POST['amount'])

		customer = stripe.Customer.create(
			email=request.POST['email'],
			name=request.POST['nickname'],
			source=request.POST['stripeToken']
			)

		charge = stripe.Charge.create(
			customer=customer,
			amount=round(amount),
			currency='usd',
			description="Shop Purchase"
			)

	return render(request, 'success.html', {'amount':amount})

def successMsg(request, args):
	amount = args
	return render(request, 'success.html', {'amount':amount})


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'welcome_page.html')
    else:
        user = request.user
        products = Product.objects.all()

    context = {
        "user": user,
        "products":products,
        "list":list,
    }
    return render(request, 'index.html', context)

def view_favorites(request):
    favs = FavoriteList.objects.filter(user=request.user)

    context = {
        "favs":favs
    }

    return render(request, 'favorites.html', context)

def view_products(request):
    products = Product.objects.all()

    context = {
        "products":products,
    }
    return render(request, 'index2.html', context)

def view_product_guest(request, product_id):
    product = Product.objects.get(pk = product_id)

    context = {
        "product":product,
    }
    return render(request, 'product_detail2.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(pk = product_id)
    cart = Cart.objects.filter(user=request.user)
    reviews = Review.objects.filter(product_id=product_id)

    form = CartListForm(request.POST or None)
    form2 = FavoriteListForm(request.POST or None)

    list = []
    for i in cart:
        list.append(i.product.id)

    # if form.is_valid():
    #     cx = form.save(commit=False)
    #     cx.user = request.user
    #     cx.product = product
    #     cx.save()
    #
    #     return redirect('/shopapp/products/'+ product_id)
    #
    # if form2.is_valid():
    #     cx = form.save(commit=False)
    #     cx.user = request.user
    #     cx.product = product
    #     cx.favorited = True
    #     cx.save()
    #
    #     return redirect('/shopapp/products/'+ product_id)

    liked = FavoriteList.objects.filter(product = product_id)
    liked = liked.first
    # obj.delete()

    if 'btnform1' in request.POST:
        cx = form.save(commit=False)
        cx.user = request.user
        cx.product = product
        cx.save()
        return redirect('/shopapp/products/'+ product_id)

    if 'btnform2' in request.POST:
        cx = form2.save(commit=False)
        cx.user = request.user
        cx.product = product
        cx.favorited = True
        cx.save()
        return redirect('/shopapp/products/'+ product_id)

    if 'btnform3' in request.POST:
        obj = get_object_or_404(FavoriteList, product__id=product_id)
        obj.delete()
        return redirect('/shopapp/products/'+ product_id)

    if 'btnform4' in request.POST:
        obj = get_object_or_404(cart, product__id=product_id)
        obj.delete()
        return redirect('/shopapp/products/'+ product_id)


    context = {
        'product': product,
        'form': form,
        'form2': form2,
        'list':list,
        'liked':liked,
        'reviews':reviews
    }
    return render(request, 'product_detail.html', context)

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST or None, initial={'user': request.user, 'product': product})

    if form.is_valid():
        cx = form.save(commit=False)
        cx.save()
        return redirect('/shopapp/products/'+ product_id)

    context = {
        "form": form,
    }

    return render(request, 'add_review.html', context)

def delete_from_cart(request, product_id):
	# cart = Cart.objects.filter(user=request.user, product__id=id)

	obj = get_object_or_404(Cart, product__id=product_id)
	obj.delete()

	return redirect('/shopapp/mycart/')

def about_us(request):
	return render(request, 'about_us.html')

def view_cart(request):
    products = Product.objects.all()
    cart = Cart.objects.filter(user=request.user)

    list = []
    for i in cart:
        list.append(i.product.id)

    context = {
        "products": products,
        "cart":cart,
        "list":list,
    }
    return render(request, 'cart.html', context)


# new user register
def sign_up(request):
    user_form = UserForm(request.POST or None)
    user_form2 = UserProfileForm(request.POST or None, request.FILES or None)


    if user_form.is_valid() and user_form2.is_valid():
        user = user_form.save(commit=False)
        username = user_form.cleaned_data['username']
        password = user_form.cleaned_data['password']
        user.set_password(password)
        user_form.save()

        userprofile = user_form2.save(commit=False)
        userprofile.user = user_form.save(commit=False)
        userprofile.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            return redirect('/shopapp')

    context = {
        "user_form": user_form,
        "user_form2": user_form2,
    }
    return render(request, 'signup.html', context)

def home(request):

    return render(request, 'homepage.html')

# User Login
def user_login(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/shopapp')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled.'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login. Please try again.'})
    return render(request, 'login.html')

# User Logout
def user_logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('/shopapp')


def profile(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=request.user)

    context = {
        "user": user,
        "userprofile":userprofile,
    }
    return render(request, 'profile.html', context)
