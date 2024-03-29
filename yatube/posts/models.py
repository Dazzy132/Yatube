from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import CreatedModel

User = get_user_model()


class AuthorRelated(models.Model):
    """Модель для наследования поля Автора"""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class Group(models.Model):
    """Группа поста"""
    title = models.CharField(
        'Группа',
        max_length=200,
        help_text='Группа, к которой будет относиться пост'
    )
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:group_list', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(AuthorRelated):
    """Модель постов"""
    MAX_LENGTH = 15

    text = models.TextField(
        'Текст поста',
        help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField('Картинка', upload_to='posts/', blank=True)

    def __str__(self):
        return self.text[:self.MAX_LENGTH]

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        default_related_name = 'posts'
        ordering = ('-pub_date',)


class Comment(AuthorRelated, CreatedModel):
    """Комментарии к постам"""
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE
    )
    text = models.TextField('Текст', help_text='Текст нового комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'


class Follow(models.Model):
    """Подписки на авторов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
