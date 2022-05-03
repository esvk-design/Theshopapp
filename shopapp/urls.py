from django.urls import path, include
from django.conf.urls import url
from . import views



app_name = 'shopapp'


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^home/$', views.home, name='home'),


    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),

    url(r'^profile/$', views.profile, name='profile'),

    url(r'^mycart/$', views.view_cart, name='view_cart'),
    url(r'^aboutus/$', views.about_us, name='about_us'),

    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^success/<str:args>/', views.successMsg, name='success'),

    url(r'^myfavs/$', views.view_favorites, name='view_favorites'),

    url(r'^products/$', views.view_products, name='view_products'),
    url(r'^products_guest/(?P<product_id>[0-9]+)/$', views.view_product_guest, name='view_product_guest'),



    url(r'^products/(?P<product_id>[0-9]+)/$', views.product_detail, name='product_detail'),



    url(r'^submit_review/(?P<product_id>[0-9]+)/$', views.add_review, name='add_review'),

    url(r'^mycart/delete/(?P<product_id>\d+)/$', views.delete_from_cart, name='delete_from_cart')

]
