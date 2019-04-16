from django.urls import path
from .views import book_list, book_detail

app_name = 'books'

urlpatterns = [
    path('', book_list, name='book-list'),
    path('<slug>/', book_detail, name='book-detail')
]
