from django.contrib import admin
from libraryusers.models import User, Favorite, Comment, Suggestion


class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('username',)}


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('book', 'user',)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('user', 'comment', 'book',)


class SuggestionAdmin(admin.ModelAdmin):
    model = Suggestion
    list_display = ('title', 'author', 'description', 'url', 'image', 'user')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
