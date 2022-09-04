from django.conf import settings
from django.core.paginator import Paginator

LIMIT_POSTS_PER_PAGE = 10


def paginate_queryset(request, queryset):
    """Функция, которая делает пагинацию страниц"""
    paginator = Paginator(queryset, settings.MAX_SHOW_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


class DataMixin:
    """Миксин, который наследуется во views.py, чтобы не задавать постоянно
    одни и те же параметры пагинации"""
    paginate_by = LIMIT_POSTS_PER_PAGE
