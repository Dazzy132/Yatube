from __future__ import annotations

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.tests.fixtures.fixtures_data import (create_group,
                                                create_post_with_group)
from posts.tests.fixtures.fixtures_user import (create_authorized_user,
                                                create_guest_user, create_user)

User = get_user_model()


class StaticURLTests(TestCase):
    """Проверка urls во всех приложениях"""

    @classmethod
    def setUpClass(cls):
        """Установка данных для тестирования"""
        super().setUpClass()
        user = create_user(User, username='author')
        create_post_with_group(user, group=create_group())
        cls.author_user = create_authorized_user(user)
        cls.responses_for_guest = {
            '/': ['posts/index.html', HTTPStatus.OK],
            '/group/test-slug/': ['posts/group_list.html', HTTPStatus.OK],
            '/profile/author/': ['posts/profile.html', HTTPStatus.OK],
            '/posts/1/': ['posts/post_detail.html', HTTPStatus.OK],
            '/posts/1/edit/': ['posts/create_post.html', HTTPStatus.FOUND],
            '/create/': ['posts/create_post.html', HTTPStatus.FOUND],
            '/about/author/': ['about/author.html', HTTPStatus.OK],
            '/about/tech/': ['about/tech.html', HTTPStatus.OK],
            '/unexisting_page/': ['core/404.html', HTTPStatus.NOT_FOUND]
        }
        cls.responses_for_auth_user = {
            '/': ['posts/index.html', HTTPStatus.OK],
            '/group/test-slug/': ['posts/group_list.html', HTTPStatus.OK],
            '/profile/test_user/': ['posts/profile.html', HTTPStatus.OK],
            '/posts/1/': ['posts/post_detail.html', HTTPStatus.OK],
            '/posts/1/edit/': ['posts/create_post.html', HTTPStatus.FOUND],
            '/create/': ['posts/create_post.html', HTTPStatus.OK],
            '/about/author/': ['about/author.html', HTTPStatus.OK],
            '/about/tech/': ['about/tech.html', HTTPStatus.OK],
            '/unexisting_page/': ['core/404.html', HTTPStatus.NOT_FOUND]
        }
        cls.responses_for_author_post = {
            '/posts/1/edit/': ['posts/create_post.html', HTTPStatus.OK],
        }

    def setUp(self):
        """Установка данных для тестирования"""
        self.guest_client = create_guest_user()
        self.user = create_user(User, username='test_user')
        self.authorized_user = create_authorized_user(self.user)

    def check_status_code(self, client: Client, responses_urls: dict):
        """Проверка статуса кода для заданного пользователя"""
        for address, (template, status) in responses_urls.items():
            with self.subTest(address=address):
                response = client.get(address)
                self.assertEqual(response.status_code, status)

    def check_template(self, client: Client, responses_urls: dict):
        """Проверка темплейта для заданного пользователя"""
        for address, (template, status) in responses_urls.items():
            with self.subTest(address=address):
                response = client.get(address)
                if response.status_code == HTTPStatus.OK:
                    self.assertTemplateUsed(response, template)
                elif response.status_code == HTTPStatus.NOT_FOUND:
                    self.assertTemplateUsed(response, template)
                # elif response.status_code == HTTPStatus.FOUND:
                #     self.assertRedirects(
                #         response, expected_url=f'/auth/login/?next={address}'
                #     )

    def test_urls_correct_status_code(self):
        """Проверка статуса кода для всех категорий пользователей"""
        client_responses = {
            self.guest_client: self.responses_for_guest,
            self.authorized_user: self.responses_for_auth_user,
            self.author_user: self.responses_for_author_post
        }
        for client, response in client_responses.items():
            self.check_status_code(client, response)

    def test_urls_correct_use_template(self):
        """Проверка используемых темплейтов для всех url """
        client_responses = {
            self.guest_client: self.responses_for_guest,
            self.authorized_user: self.responses_for_auth_user,
            self.author_user: self.responses_for_author_post
        }
        for client, response in client_responses.items():
            self.check_template(client, response)
