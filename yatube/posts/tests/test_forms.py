import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post
from posts.tests.fixtures.fixtures_data import create_post
from posts.tests.fixtures.fixtures_user import (create_authorized_user,
                                                create_guest_user, create_user)

# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


# Для сохранения media-файлов в тестах будет использоваться
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Установка данных для тестирования"""
        super().setUpClass()
        cls.user = create_user(User, username='test_user2')
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        """Удаление временной temp папки"""
        super().tearDownClass()
        # Модуль shutil - библиотека Python с удобными инструментами
        # для управления файлами и директориями: создание, удаление,
        # копирование, перемещение, изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Установка данных для тестирования"""
        # Создаем неавторизованный клиент
        self.guest_client = create_guest_user()
        self.auth_user = create_authorized_user(self.user)

    def test_create_and_edit_this_post(self):
        """Валидная форма создает запись в Post и редактирует."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()

        # Для тестирования загрузки изображений
        # берём байт-последовательность картинки,
        # состоящей из двух пикселей: белого и чёрного
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        # Эмуляция загрузки картинки
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'text': 'Тестовый текст',
            'author': self.user,
            'image': uploaded,
        }

        # Отправляем POST-запрос
        # Если вы установите follow в True, клиент будет следовать любым
        # перенаправлениям, а в объекте ответа будет установлен атрибут
        # redirect_chain, содержащий кортежи промежуточных адресов и кодов
        # состояния.
        response = self.auth_user.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        # Проверяем, сработал ли редирект
        self.assertRedirects(response,
                             reverse('posts:profile', args=[self.user]))

        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)

        # Проверяем, что создалась запись с заданными полями
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                author=self.user
            ).exists()
        )

        # Проверка на изменение поста
        form_data = {
            'text': 'Текст измененного поста',
            'author': self.user,
        }

        response = self.auth_user.post(
            reverse('posts:post_edit', args=[1]),
            data=form_data,
            follow=True
        )

        # Проверка, что при изменении поста редирект был на измененный пост
        self.assertRedirects(response, reverse('posts:post_detail', args=[1]))

        # Проверка на то, что кол-во постов не прибавилось (изначально было 0)
        self.assertEqual(Post.objects.count(), posts_count + 1)

        # Проверка на то, что пост обновился и он существует
        self.assertTrue(
            Post.objects.filter(
                text='Текст измененного поста',
                author=self.user
            ).exists()
        )

        # Проверка, что пост действительно был изменен
        self.assertFalse(
            Post.objects.filter(
                text='Тестовый текст',
                author=self.user
            ).exists()
        )

    def test_signup_user(self):
        """Проверка работы регистрационной формы"""
        form_data_user = {
            'first_name': 'Иван',
            'last_name': 'Иванович',
            'username': 'ivanushka',
            'email': 'ivanushka@mail.ru',
            'password1': '123456',
            'password2': '123456',
        }

        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data_user,
            follow=True
        )

        # Проверяем что пользователя перенесло на главную страницу
        self.assertRedirects(response, reverse('posts:index'))

        # Проверка на то, что пользователь был создан
        self.assertTrue(
            User.objects.filter(
                username='ivanushka'
            )
        )

    def test_add_comment(self):
        """Проверка на то, что только авторизованный пользователь может
        комментировать пост. И после отправки комментария он добавляется на
        страницу поста"""

        post = create_post(self.user)

        comment_form_data = {
            'text': 'Текст комментария'
        }

        response_guest = self.guest_client.post(
            reverse('posts:add_comment', args=[1]),
            data=comment_form_data,
            follow=True
        )

        # Неавторизованный пользователь получит страницу авторизации
        self.assertRedirects(
            response_guest, '/auth/login/?next=/posts/1/comment/'
        )

        response_auth_user = self.auth_user.post(
            reverse('posts:add_comment', args=[1]),
            data=comment_form_data,
            follow=True
        )

        # После отправки поста он отправляется на детальный просмотр поста
        self.assertEqual(response_auth_user.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response_auth_user, reverse('posts:post_detail', args=[1])
        )

        # Проверка на то, что комментарий создался у поста
        self.assertEqual(post.comments.count(), 1)

        post_detail = self.auth_user.get(
            reverse('posts:post_detail', args=[1])
        )

        # В контексте страницы у поста есть комментарий
        self.assertEqual(post_detail.context['post'].comments.count(), 1)
