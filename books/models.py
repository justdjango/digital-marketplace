from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.shortcuts import redirect, reverse

'''
Author
    Book
        Chapter 1
            Exercise 1
                Solution 1
                Solution 2
                ...
            Exercise 2
            ..
        Chapter 2
'''


class UserLibrary(models.Model):
    books = models.ManyToManyField('Book', blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def book_list(self):
        return self.books.all()

    class Meta:
        verbose_name = 'User Library'
        verbose_name_plural = 'User Library'


def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserLibrary.objects.get_or_create(user=instance)


post_save.connect(post_user_signup_receiver, sender=settings.AUTH_USER_MODEL)


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)
    publication_date = models.DateTimeField()
    isbn = models.CharField(max_length=16)
    slug = models.SlugField()
    cover = models.ImageField()
    price = models.FloatField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:book-detail", kwargs={
            'slug': self.slug
        })


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:chapter-detail", kwargs={
            'book_slug': self.book.slug,
            'chapter_number': self.chapter_number
        })


class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    exercise_number = models.IntegerField()
    page_number = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:exercise-detail", kwargs={
            'book_slug': self.chapter.book.slug,
            'chapter_number': self.chapter.chapter_number,
            'exercise_number': self.exercise_number
        })


class Solution(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    solution_number = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return f"{self.exercise.title}-{self.pk}"
