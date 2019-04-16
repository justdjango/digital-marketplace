from django.shortcuts import render, get_object_or_404
from .models import Book


def book_list(request):
    queryset = Book.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, "book_list.html", context)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    context = {
        'book': book
    }
    return render(request, "book_detail.html", context)
