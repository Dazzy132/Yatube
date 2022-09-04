from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    """Страница об Авторе"""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Страница о Технологиях"""
    template_name = 'about/tech.html'
