from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Отображение БД Постов в админке"""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group', 'get_photo')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    save_as = True
    empty_value_display = '-пусто-'

    def get_photo(self, obj):
        """Метод отображения картинки поста в админке"""
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="100" height="110"'
            )
        return '----'

    # Изменить название метода на понятный
    get_photo.short_description = 'Фотография поста'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Отображение БД Групп в админке"""
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображение БД Комментариев в админке"""
    list_display = ('author', 'post', 'created')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Отображение БД Подписок в админке"""
    list_display = ('user', 'author')