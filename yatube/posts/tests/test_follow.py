from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Follow
from posts.tests.fixtures.fixtures_data import create_post
from posts.tests.fixtures.fixtures_user import (create_authorized_user,
                                                create_guest_user, create_user)

User = get_user_model()


class TestFollow(TestCase):
    """Проверка системы подписок"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = create_user(User, username='TestFollowerUser')
        cls.user2 = create_user(User, username='TestFollowingUser')
        cls.user3 = create_user(User, username='Jamshut')
        cls.post = create_post(cls.user2, 'Текст постика')

    def setUp(self):
        self.guest_client = create_guest_user()
        self.auth_user = create_authorized_user(self.user)
        self.auth_user2 = create_authorized_user(self.user3)

    def test_user_can_subscribe(self):
        """Проверка на то, что авторизованный пользователь сможет подписаться,
        неавторизованный получит редирект, и пост отображается там, где ему
        положено быть"""

        # Генерировать запрос на подписку
        self.auth_user.get(
            reverse('posts:profile_follow', args=[self.user2])
        )

        # Проверить, что подписка была осуществлена
        self.assertTrue(
            Follow.objects.filter(user=self.user, author=self.user2).exists()
        )

        # Генерировать попытку подписаться от анонимного пользователя
        response = self.guest_client.get(
            reverse('posts:profile_follow', args=[self.user2])
        )

        # Он должен будет быть отправлен на страницу авторизации с переходом
        self.assertRedirects(
            response, '/auth/login/?next=/profile/TestFollowingUser/follow/'
        )

        # Переход на страницу пользователя, который был подписан на автора
        response = self.auth_user.get(reverse('posts:follow_index'))
        # Проверка на то, что пост избранного автора отразился
        self.assertIn(self.post, response.context['page_obj'])

        # Проверка на то, что у пользователя Джамшут не отобразился этот пост
        response = self.auth_user2.get(reverse('posts:follow_index'))
        self.assertNotIn(self.post, response.context['page_obj'])

        # Проверка на то, что если пользователь попытается подписаться на себя
        # то у него ничего не выйдет
        response = self.auth_user.get(
            reverse('posts:profile_follow', args=[self.user])
        )

        # Пользователь не может на себя подписаться
        self.assertFalse(
            Follow.objects.filter(user=self.user, author=self.user).exists()
        )
