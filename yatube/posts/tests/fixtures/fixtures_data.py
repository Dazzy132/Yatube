from django.contrib.auth import get_user_model
from mixer.backend.django import mixer as _mixer

from posts.models import Group, Post

User = get_user_model()


def create_post(user: User, text=None) -> Post:
    """Создать тестовый пост"""
    return Post.objects.create(text=text or 'Текст поста', author=user)


def create_group(title=None, desc=None, slug=None) -> Group:
    """Создать тестовую группу"""
    return Group.objects.create(
        title=title or 'Тестовая группа',
        description=desc or 'Описание тестовой группы',
        slug=slug or 'test-slug'
    )


def create_post_with_group(user: User, group: Group) -> Post:
    """Создать один пост с группой"""
    return Post.objects.create(text='Текст поста', author=user, group=group)


def few_posts_with_group(user: User, group: Group):
    """Возвращает несколько постов созданных с группой"""
    posts = _mixer.cycle(25).blend(Post,
                                   author=user,
                                   group=group,
                                   text='Текст поста')
    return posts[0]
