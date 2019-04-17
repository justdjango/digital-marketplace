from django.contrib import admin
from .models import Author, Book, Chapter, Exercise, Solution, UserLibrary

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Exercise)
admin.site.register(Solution)
admin.site.register(UserLibrary)
