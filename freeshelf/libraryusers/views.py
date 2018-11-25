from django.shortcuts import render, redirect
from libraryusers.forms import CustomUserCreationForm, SuggestionForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from libraryusers.models import User, Favorite, Suggestion
from django.contrib.auth.decorators import login_required
from library.models import Book, Category
from django.http import HttpResponse, Http404
import json
from django.template.defaultfilters import slugify
from django.contrib.admin.views.decorators import staff_member_required


def register(request):
    form_class = CustomUserCreationForm

    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.slug = slugify(username)
            user.save()

            user = authenticate(username=username,
                                password=password)

            login(request, user)
            return redirect('home')

        else:
            return render(request, 'register.html', {
                'form': form,
            })

    form = form_class()
    return render(request, 'register.html', {
        'form': form
    })


def user_login(request):
    form_class = AuthenticationForm

    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        else:
            return render(request, 'login.html', {
                'form': form,
                'errors': form.errors
            })

    form = form_class()
    return render(request, 'login.html', {
        'form': form
    })


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def favorites(request):
    favorites = request.user.favorite_set.all()
    books = [item.book for item in favorites]
    return render(request, 'favorites.html', {
        'books': books
    })


@login_required
def favorite_book(request):
    if request.method == "POST":
        slug = request.POST['slug']
        book = Book.objects.get(slug=slug)
        user = request.user

        if book in [favorite.book for favorite in user.favorite_set.all()]:
            remove_favorite = user.favorite_set.get(book=book)

            remove_favorite.delete()
            return HttpResponse(json.dumps(["removed", slug]))
        else:
            new_favorite = Favorite(book=book, user=user)
            new_favorite.save()
            return HttpResponse(json.dumps(["added", slug]))

    else:
        return Http404()


def user_profile(request, slug):
    user = User.objects.get(slug=slug)
    comments = user.comment_set.all()
    return render(request, 'user_profile.html', {
        'user': user,
        'comments': comments
    })


@login_required
def suggestions(request):
    form_class = SuggestionForm
    suggestions = Suggestion.objects.all()

    if request.method == "POST":
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            Suggestion.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                description=form.cleaned_data['description'],
                url=form.cleaned_data['url'],
                image=form.cleaned_data['image'],
                slug=slugify(form.cleaned_data['title']),
                user=request.user,
            )

    form = form_class()
    return render(request, 'suggestions.html', {
        'suggestions': suggestions,
        'form': form
    })


@staff_member_required
def handle_suggestion(request):
    if request.method == "POST":
        confirmation = request.POST['confirmation']
        suggestion = Suggestion.objects.get(slug=request.POST['book-slug'])

        if confirmation == "confirm":
            book = Book(
                    title=suggestion.title,
                    author=suggestion.author,
                    description=suggestion.description,
                    url=suggestion.url,
                    slug=slugify(suggestion.title)
            )
            if suggestion.image:
                book.image = suggestion.image
            suggestion.delete()
            book.save()

            return HttpResponse(json.dumps(["success"]))
        elif confirmation == "decline":
            suggestion.delete()

            return HttpResponse(json.dumps(["success"]))
    else:
        return Http404()
