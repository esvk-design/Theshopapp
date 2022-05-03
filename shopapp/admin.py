from django.contrib import admin
from .models import Department, Review, Product, UserProfile, Cart, FavoriteList

# Register your models here.
admin.site.register(Department)
admin.site.register(Review)
admin.site.register(Product)

admin.site.register(UserProfile)

admin.site.register(Cart)
admin.site.register(FavoriteList)
