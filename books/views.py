from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter


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
    context = {
        'book': book
    }
    return render(request, "book_detail.html", context)


def chapter_detail(request, book_slug, chapter_number):
    chapter_qs = Chapter.objects \
        .filter(book__slug=book_slug) \
        .filter(chapter_number=chapter_number)
    if chapter_qs.exists():
        context = {
            'chapter': chapter_qs[0]
        }
        return render(request, "chapter_detail.html", context)
    return Http404
