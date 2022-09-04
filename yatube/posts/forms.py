from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма создания новых постов"""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Форма создания комментариев к постам"""
    class Meta:
        model = Comment
        fields = ('text',)
