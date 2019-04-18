from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Exercise
from shopping_cart.models import Order, OrderItem

OWNED = 'owned'
IN_CART = 'in_cart'
NOT_IN_CART = 'not_in_cart'


def check_book_relationship(request, book):
    if book in request.user.userlibrary.book_list():
        return OWNED
    order_qs = Order.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        order_item_qs = OrderItem.objects.filter(book=book)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item in order.items.all():
                return IN_CART
    return NOT_IN_CART


def book_list(request):
    # display a list of the books
    queryset = Book.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, "book_list.html", context)


@login_required
def book_detail(request, slug):
    # display a list of the chapters in this book
    book = get_object_or_404(Book, slug=slug)
    book_status = check_book_relationship(request, book)
    context = {
        'book': book,
        'book_status': book_status
    }
    return render(request, "book_detail.html", context)


@login_required
def chapter_detail(request, book_slug, chapter_number):
    # display a list of the exercises in the chapter
    chapter_qs = Chapter.objects \
        .filter(book__slug=book_slug) \
        .filter(chapter_number=chapter_number)
    chapter = chapter_qs[0]
    book_status = check_book_relationship(request, chapter.book)
    if chapter_qs.exists():
        context = {
            'chapter': chapter,
            'book_status': book_status
        }
        return render(request, "chapter_detail.html", context)
    return Http404


@login_required
def exercise_detail(request, book_slug, chapter_number, exercise_number):
    exercise_qs = Exercise.objects \
        .filter(chapter__book__slug=book_slug) \
        .filter(chapter__chapter_number=chapter_number) \
        .filter(exercise_number=exercise_number)
    exercise = exercise_qs[0]
    book_status = check_book_relationship(request, exercise.chapter.book)
    if exercise_qs.exists():
        context = {
            'exercise': exercise,
            'book_status': book_status
        }
        return render(request, "exercise_detail.html", context)
    return Http404
