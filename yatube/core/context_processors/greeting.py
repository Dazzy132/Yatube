def welcome(request):
    """Добавляет в контекст переменную greeting с приветствием."""
    return {
        'greeting': 'Добро пожаловать!'
    }
