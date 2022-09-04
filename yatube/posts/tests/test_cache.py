from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.tests.fixtures.fixtures_data import create_post
from posts.tests.fixtures.fixtures_user import (create_authorized_user,
                                                create_user)

User = get_user_model()


class TestCacheView(TestCase):
    """Проверка кеширования"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = create_user(User, 'TestUserok')
        cls.cache_post = create_post(cls.user, 'text_posta')

    def setUp(self):
        self.auth_user = create_authorized_user(self.user)

    def test_cache_index_page(self):
        """Проверка на то, что пост останется в кеше странице, но при этом
        он будет удален"""
        response = self.auth_user.get(reverse('posts:index'))
        assert self.cache_post in response.context['page_obj']
        self.cache_post.delete()
        response = self.auth_user.get(reverse('posts:index'))
        self.assertIn(self.cache_post.text, response.content.decode())
