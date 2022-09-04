import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Page
from django.test import TestCase, override_settings
from django.urls import reverse

from posts.models import Post
from posts.tests.fixtures.fixtures_data import (create_group, create_post,
                                                create_post_with_group,
                                                few_posts_with_group)
from posts.tests.fixtures.fixtures_user import (create_authorized_user,
                                                create_user)

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """Установка основных данных для тестирования"""
        super().setUpClass()
        cls.user = create_user(User, username='test_user')
        cls.auth_user = create_authorized_user(cls.user)
        group = create_group()
        cls.group2 = create_group(
            'Тестовая группа 2',
            'Описание',
            'test-slug2'
        )
        # Создание постов
        few_posts_with_group(cls.user, group=group)
        # Константы
        cls.MAX_POSTS_PER_PAGE = 10
        cls.MAX_POSTS_COUNT = 25
        cls.MAX_PAGES_COUNT = 3
        cls.MAX_POSTS_COUNT_END_PAGE = 5

    @classmethod
    def tearDownClass(cls):
        """Удаление временной temp папки"""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    args=['test-slug']): 'posts/group_list.html',
            reverse('posts:profile', args=['test_user']): 'posts/profile.html',
            reverse('posts:post_detail', args=[5]): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', args=[7]): 'posts/create_post.html',
            reverse('about:tech'): 'about/tech.html',
            reverse('about:author'): 'about/author.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:signup'): 'users/signup.html',
            reverse(
                'users:password_change'): 'users/password_change_form.html',
            reverse(
                'users:password_change_done'
            ): 'users/password_change_done.html',
            reverse('users:password_reset'): 'users/password_reset_form.html',
            reverse(
                'users:password_reset_done'): 'users/password_reset_done.html',
            reverse(
                'users:reset_confirm',
                args=['NA', '634-7f7ae6246fbf719c4215']
            ): 'users/password_reset_confirm.html',
            reverse(
                'users:reset_complete'): 'users/password_reset_complete.html',
            reverse('users:logout'): 'users/logged_out.html',
        }

        # Проверка на то, какой теймплейт использует view функция
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.auth_user.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_context_in_url(self, context: str, reverse_url: str):
        """Проверяет наличие контекста на заданном url"""
        response = self.auth_user.get(reverse_url)
        assert context in response.context, (
            f'Контекст не передан в {reverse_url} '
        )
        context_obj = response.context[context]
        return context_obj

    def check_context_page_obj(self, obj: Page):
        """Проверка, что контекст - объект Page и работает правильно """
        assert isinstance(obj, Page), 'Объект не Page'
        assert obj.paginator.per_page == self.MAX_POSTS_PER_PAGE, (
            'Максимум объектов на странице 10'
        )
        assert obj.paginator.count == self.MAX_POSTS_COUNT, (
            'Созданных постов должно быть 25'
        )
        assert obj.has_other_pages() is True, (
            'У объекта должны быть дополнительные страницы'
        )
        assert obj.paginator.num_pages == self.MAX_PAGES_COUNT, (
            'Страниц должно быть 3'
        )
        start_page = obj.paginator.get_page(1)
        end_page = obj.paginator.get_page(3)
        assert len(start_page) == self.MAX_POSTS_PER_PAGE, (
            'На первой странице должно быть 10 постов'
        )
        assert len(end_page) == self.MAX_POSTS_COUNT_END_PAGE, (
            'На последней странице должно быть 5 постов'
        )

    def test_context_index(self):
        """Проверка контекста главной страницы"""
        obj = self.check_context_in_url('page_obj', reverse('posts:index'))
        self.check_context_page_obj(obj)

    def test_context_group_list(self):
        """Проверка контекста страниц групп"""
        # Проверка на то, что у тестовой группы есть контекст
        obj = self.check_context_in_url(
            'page_obj', reverse('posts:group_list', args=['test-slug'])
        )
        # Проверка на то, что объект - Page
        self.check_context_page_obj(obj)

        # Создание поста относящегося к другой группе
        other_group_post = create_post_with_group(self.user, self.group2)

        # Проверка на то, что этого поста нет в контексте другой группы
        assert other_group_post not in obj, (
            'Пост не должен выводится не в своей группе'
        )

        # Проверка, что новый пост выводится на главную
        index = self.check_context_in_url('page_obj', reverse('posts:index'))
        assert other_group_post in index, 'Пост должен выводится на главной'

        # Проверка, что пост выводится на странице своей группы
        post = self.check_context_in_url(
            'page_obj', reverse('posts:group_list',
                                args=[other_group_post.group.slug])
        )
        assert other_group_post in post, 'Пост должен выводится в своей группе'

    def test_context_user_profile(self):
        """Проверка профиля пользователя"""
        obj = self.check_context_in_url(
            'page_obj', reverse('posts:profile', args=[self.user])
        )
        self.check_context_page_obj(obj)

        # Проверка на то, что автор первого поста в профиле - автор профиля
        obj1 = obj.object_list[0]
        self.assertEqual(obj1.author.username, self.user.username)

        # Проверка, что созданный пост отобразится в профиле
        new_post = create_post(self.user, text='Новый пост в профиле')
        new_response = self.check_context_in_url(
            'page_obj', reverse('posts:profile', args=[self.user])
        )
        assert new_post in new_response, (
            'Новые посты пользователя должны отображаться в профиле'
        )

    def test_post_detail_context(self):
        """Проверка детального просмотра записи"""
        post = self.check_context_in_url(
            'post', reverse('posts:post_detail', args=[1])
        )
        assert post.pk == 1, 'id поста должен совпадать с указанным id'

    def test_create_post_context(self):
        """Проверка формы создания поста"""
        form = self.check_context_in_url('form', reverse('posts:post_create'))
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
        }

        # Проверка каждого поля на тип данных
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_context(self):
        """Проверка формы редактирования поста"""
        form = self.check_context_in_url(
            'form', reverse('posts:post_edit', args=[1])
        )
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)
