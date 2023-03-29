from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.urls import path, include

from . import views

app_name = 'users'

authorization_patterns = [
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/',
         views.SignUp.as_view(),
         name='signup'),
]

password_patterns = [
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change_form.html'
         ),
         name='password_change'),
    path('password_change/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_change_done.html'
         ),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
]

recovery_patterns = [
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='reset_confirm'),

    path('reset/done',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='reset_complete'),
]

urlpatterns = [
    # Авторизация/Выход/Регистрация
    path('', include(authorization_patterns)),
    # Изменение пароля/Восстановление пароля
    path('', include(password_patterns)),
    # Ссылки на восстановление аккаунта
    path('', include(recovery_patterns)),
]
