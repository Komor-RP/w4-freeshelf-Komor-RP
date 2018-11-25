from django.contrib import admin
from django.urls import path
from library import views as library_views
from libraryusers import views as user_views
from django.conf import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('', library_views.index, name='home'),
    path('books/', library_views.get_books, name="all_books"),
    path('sort_books/', library_views.sort_books, name="sort_books"),
    path('books/<slug>/', library_views.book_detail, name="book_detail"),
    path('books/<slug>/edit', library_views.edit_book, name="edit_book"),
    path('books/<slug>/delete', library_views.delete_book, name="delete_book"),
    path('books/new', library_views.create_book, name="create_book"),
    path('categories/', library_views.categories, name="categories"),
    path('categories/<slug>',
         library_views.category_detail, name="category_detail"),
    path('favorites/', user_views.favorites, name="favorites"),
    path('favorite_book/', user_views.favorite_book, name="favorite_book"),
    path('users/<slug>', user_views.user_profile, name="user_profile"),
    path('suggestions/', user_views.suggestions, name="suggestions"),
    path('handle_suggestion/',
         user_views.handle_suggestion,
         name="handle_suggestion"),
    path('register/', user_views.register, name="register"),
    path('login/', user_views.user_login, name="login"),
    path('logout/', user_views.user_logout, name="logout"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
