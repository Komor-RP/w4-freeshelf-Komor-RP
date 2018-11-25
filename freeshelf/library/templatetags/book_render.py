from django import template
from library.models import Book

register = template.Library()


@register.inclusion_tag('books/book_render.html')
def book_render(user, books):
    return {
        'user': user,
        'books': books
    }
