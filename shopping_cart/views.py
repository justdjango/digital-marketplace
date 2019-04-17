from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from books.models import Book
from .models import Order, OrderItem


def add_to_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item = OrderItem.objects.create(book=book)
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
