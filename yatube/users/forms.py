from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """Форма для регистрации пользователей"""

    class Meta(UserCreationForm.Meta):
        """Переопределение полей"""
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
