from django.shortcuts import render
from library.models import Book, Category
from libraryusers.models import Comment
from django.http import Http404
from libraryusers.forms import CommentCreation


def index(request):
    books = Book.objects.all()

    return render(request, 'index.html', {
        'books': books
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, 'category/index.html', {
        'categories': categories
    })


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    books = category.books.all
    return render(request, 'category/category_detail.html', {
        'category': category,
        'books': books
    })


def book_detail(request, slug):
    form_class = CommentCreation
    book = Book.objects.get(slug=slug)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = request.user
            comment_text = form.cleaned_data['comment']
            comment = Comment(user=user, book=book, comment=comment_text)
            comment.save()

    form = form_class()
    comments = book.comment_set.all()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'form': form,
        'comments': comments
    })


def sort_books(request):
    if request.method == "GET":
        if request.is_ajax():
            user = request.user
            books = Book.objects.all()
            if request.GET['sort_method'] == "title-ascending":
                books = books.order_by('title')
            elif request.GET['sort_method'] == "date-ascending":
                books = books.order_by('created')

            return render(request, 'books/book_render.html', {
                'user': user,
                'books': books
            })


def get_books(request):
    books = Book.objects.all()
    return render(request, 'books/books.html', {
        'books': books,
    })
