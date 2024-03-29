from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    """Вывод страницы ошибки с кодом 404. exception в себе содержит всю
    отладочную информацию"""
    return render(request, 'core/404.html', {'path': request.path},
                  status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    """Вывод страницы ошибки с кодом """
    return render(request, 'core/403csrf.html', status=HTTPStatus.FORBIDDEN)


def internal_server_error(request):
    """Вывод страницы с ошибкой Internal Server Error"""
    return render(request, 'core/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)
