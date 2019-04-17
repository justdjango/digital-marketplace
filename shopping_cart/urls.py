from django.urls import path
from .views import add_to_cart

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/<book_slug>/', add_to_cart, name='add-to-cart')
]
