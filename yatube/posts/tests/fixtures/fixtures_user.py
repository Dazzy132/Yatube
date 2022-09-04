from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


# django_user_model
def create_user(django_user_model, username):
    """Создает тестового пользователя"""
    return django_user_model.objects.create_user(username=username)


def create_guest_user():
    """Создает неавторизованного пользователя"""
    guest_user = Client()
    return guest_user


def create_authorized_user(user):
    """Создать авторизованного пользователя"""
    auth_user = Client()
    auth_user.force_login(user)
    return auth_user
