from django.db import models
from django.contrib.auth.models import AbstractUser
from library.models import Book, Timestamp


class User(AbstractUser):
    slug = models.SlugField(unique=True)
    USERNAME_FIELD = 'username'


class Favorite(Timestamp):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title


class Comment(Timestamp):
    comment = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
