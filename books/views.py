from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Exercise
from shopping_cart.models import Order, OrderItem


def book_list(request):
    # display a list of the books
    queryset = Book.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, "book_list.html", context)


def book_detail(request, slug):
    # display a list of the chapters in this book
    book = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(user=request.user)
    book_is_in_cart = False
    if order_qs.exists():
        order = order_qs[0]
        order_item_qs = OrderItem.objects.filter(book=book)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item in order.items.all():
                book_is_in_cart = True
    context = {
        'book': book,
        'in_cart': book_is_in_cart
    }
    return render(request, "book_detail.html", context)


def chapter_detail(request, book_slug, chapter_number):
    # display a list of the exercises in the chapter
    chapter_qs = Chapter.objects \
        .filter(book__slug=book_slug) \
        .filter(chapter_number=chapter_number)
    if chapter_qs.exists():
        context = {
            'chapter': chapter_qs[0]
        }
        return render(request, "chapter_detail.html", context)
    return Http404


def exercise_detail(request, book_slug, chapter_number, exercise_number):
    exercise_qs = Exercise.objects \
        .filter(chapter__book__slug=book_slug) \
        .filter(chapter__chapter_number=chapter_number) \
        .filter(exercise_number=exercise_number)
    if exercise_qs.exists():
        context = {
            'exercise': exercise_qs[0]
        }
        return render(request, "exercise_detail.html", context)
    return Http404
