from django.contrib import admin
from library.models import Book, Category


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ('title', 'author', 'description', 'url', 'image')
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
