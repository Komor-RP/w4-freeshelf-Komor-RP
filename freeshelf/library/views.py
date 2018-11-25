from django.shortcuts import render, redirect
from library.models import Book, Category
from libraryusers.models import Comment
from libraryusers.forms import CommentCreation
from library.forms import BookForm
from django.template.defaultfilters import slugify
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'categories': categories,
        'books': books,
    })


def get_books(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'books/books.html', {
        'categories': categories,
        'books': books,
    })


def book_detail(request, slug):
    categories = Category.objects.all()
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
        'categories': categories,
        'book': book,
        'form': form,
        'comments': comments
    })


@staff_member_required
def edit_book(request, slug):
    categories = Category.objects.all()
    form_class = BookForm
    book = Book.objects.get(slug=slug)
    if request.method == "POST":
        form = form_class(data=request.POST, files=request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', slug=book.slug)

    else:
        form = form_class(instance=book)

    return render(request, 'books/edit_book.html', {
        'categories': categories,
        'book': book,
        'form': form
    })


@staff_member_required
def create_book(request):
    categories = Category.objects.all()
    form_class = BookForm

    if request.method == "POST":
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.name)
            book.save()
            return redirect('book_detail', slug=book.slug)

    else:
        form = form_class()

    return render(request, 'books/create_book.html', {
        'categories': categories,
        'form': form
    })

@staff_member_required
def delete_book(request, slug):
    book = Book.objects.get(slug=slug)
    book.delete()
    return redirect('all_books')


def sort_books(request):
    categories = Category.objects.all()
    if request.method == "GET":
        if request.is_ajax():
            user = request.user
            books = Book.objects.all()
            if request.GET['sort_method'] == "title-ascending":
                books = books.order_by('title')
            elif request.GET['sort_method'] == "date-ascending":
                books = books.order_by('-created')

            return render(request, 'books/book_render.html', {
                'categories': categories,
                'user': user,
                'books': books
            })


def categories(request):
    categories = Category.objects.all()
    return render(request, 'category/index.html', {
        'categories': categories
    })


def category_detail(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    books = category.books.all
    return render(request, 'category/category_detail.html', {
        'categories': categories,
        'category': category,
        'books': books
    })
