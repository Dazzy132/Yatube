from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.tests.fixtures.fixtures_data import create_group, create_post
from posts.tests.fixtures.fixtures_user import create_user

User = get_user_model()


class PostModelTest(TestCase):
    """Тестирование моделей"""

    @classmethod
    def setUpClass(cls):
        """Подготовка для тестов"""
        super().setUpClass()
        user = create_user(User, username='auth')
        cls.group = create_group('Тестовая группа',
                                 'Тестовое описание',
                                 'Тестовый слаг', )
        cls.test_post = create_post(user, 'Тестовый пост')
        cls.long_title_post = create_post(user, '12345678901234567890')

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        self.assertEqual(str(self.test_post), self.test_post.text[:15])
        self.assertEqual(
            str(self.long_title_post), self.long_title_post.text[:15])
        self.assertEqual(str(self.group), self.group.title)

    def test_models_posts_have_correct_help_text(self):
        """Проверка корректности хелп текстов у модели"""
        field_help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.test_post._meta
                    .get_field(field).help_text, expected_value)

    def test_models_have_correct_verbose_name(self):
        """Проверка на правильное отображение имен"""
        field_verbose_names = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, excepted_value in field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.test_post
                    ._meta.get_field(field).verbose_name, excepted_value)
