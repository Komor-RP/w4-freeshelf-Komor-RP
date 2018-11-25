from django.contrib import admin
from libraryusers.models import User, Favorite, Comment


class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('username',)}


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('book', 'user',)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('user', 'comment', 'book',)


admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment, CommentAdmin)
