from django.urls import path
from .views import (
    book_list,
    book_detail,
    chapter_detail,
    exercise_detail
)

app_name = 'books'

urlpatterns = [
    path('', book_list, name='book-list'),
    path('<slug>/', book_detail, name='book-detail'),
    path('<book_slug>/<chapter_number>',
         chapter_detail,
         name='chapter-detail'),
    path('<book_slug>/<chapter_number>/<exercise_number>/',
         exercise_detail,
         name='exercise-detail')
]
