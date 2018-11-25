from django.forms import ModelForm
from library.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'url', 'image',)