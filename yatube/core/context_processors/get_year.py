from datetime import date


def year(request):
    """Получить текущий год"""
    return {
        "year": date.today().year
    }
