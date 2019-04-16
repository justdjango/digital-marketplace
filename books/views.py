from django.shortcuts import render
from .models import Book


def book_list(request):
    queryset = Book.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, "book_list.html", context)
