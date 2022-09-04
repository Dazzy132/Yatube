from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    """Форма регистрации пользователей (Переопределена)"""
    form_class = CreationForm
    # Ленивые ссылки перенаправляют после отработки кода
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
