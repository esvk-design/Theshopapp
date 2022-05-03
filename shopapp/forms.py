from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile, Cart, FavoriteList, Review
import datetime
from django.contrib.auth.forms import UserChangeForm



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
         model = User
         fields = ['username', 'email','first_name', 'last_name']

class UserProfileForm(forms.ModelForm):

    class Meta:
         model = UserProfile
         fields = ['address','phone']

class CartListForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product']

class FavoriteListForm(forms.ModelForm):
    class Meta:
        model = FavoriteList
        fields = ('user', 'product', 'favorited')

class ReviewForm(forms.ModelForm):
    review_message = forms.CharField(widget=forms.Textarea(attrs={'rows': '3','cols': '25',}),)

    class Meta:
        model = Review
        fields = ['user','product', 'review_message']
