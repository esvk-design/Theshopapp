from django.contrib.auth.models import Permission, User
from datetime import datetime
from django.db import models
from decimal import Decimal
from django.core import validators


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.department_name)

class Product(models.Model):
    brand = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=400)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    price = models.FloatField(null=True, blank=True, default=None)
    s_choices = (('New','New'),('Certified','Certified'),('Used','Used'),)
    status = models.CharField(max_length=10,choices=s_choices, default='New')
    photo1 = models.ImageField(upload_to='place_images', blank=True)
    photo2 = models.ImageField(upload_to='place_images', blank=True)

    def __str__(self):
        return str(self.title)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_message = models.CharField(max_length=10000)
    date_posted = models.DateField(auto_now=True)
    # date_posted = models.DateField(default=timezone.now)


    def __str__(self):
        return str(self.product)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=30, default="Title")
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return str(self.user.first_name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return str(self.user)

class FavoriteList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True)
    favorited = models.BooleanField(default=False)

    def __str__(self):
         return str(self.user)+ ', ' + str(self.product)


from django.db import models
from django.core import validators


class OrderDetail(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(
        verbose_name='Customer Email'
    )

    product = models.ForeignKey(
        to=Product,
        verbose_name='Product',
        on_delete=models.PROTECT
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    stripe_payment_intent = models.CharField(
        max_length=200
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )
