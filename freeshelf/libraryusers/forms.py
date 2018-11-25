from django.contrib.auth.forms import UserCreationForm
from libraryusers.models import User, Comment, Suggestion
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class CommentCreation(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ('title', 'author', 'description', 'url', 'image',)
