from django.urls import path
from .views import (
    add_to_cart,
    remove_from_cart,
    order_view,
    checkout
)

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/<book_slug>/',
         add_to_cart,
         name='add-to-cart'),
    path('remove-from-cart/<book_slug>/',
         remove_from_cart,
         name='remove-from-cart'),
    path('order-summary/', order_view, name='order-summary'),
    path('checkout/', checkout, name='checkout')
]
