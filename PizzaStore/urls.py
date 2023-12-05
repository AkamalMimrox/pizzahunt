

from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('detail/<str:slug>',views.detail,name="detail"),
    path('menu',views.menu,name="menu"),
    path('about',views.about_view,name="about"),
    path('book',views.book,name="book"),
    
    
    
    
    
    #cart
    
    path('cart',views.cart,name='cart'),
    
    #add to cart
    
    path('add-to-cart/<str:slug>',views.add_to_cart,name='addTocart'),
    #path('add-to-cart/',views.add_to_cart,name='addTocart'),
    
    #remove item from cart
    
    path('remove/<str:slug>',views.removeitem,name="removeitem"),
    
    #increment quantity
    
    path('increment/<str:slug>',views.increment,name='increment'),
    
    #decrement quantity
    
    path('decrement/<str:slug>',views.decrement,name='decrement'),
    
    #checkout
    
    path('checkout/',views.checkout,name='checkout'),
    
    #orders 
    
    path('orders/' ,views.orders,name='orders')
    
    
    
    
]
