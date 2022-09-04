from django import template

register = template.Library()


# Декоратор, меняющий поведение функций
@register.filter
def addclass(field, css):
    """Функция добавления фильтра к полям формы
    {{ field|addclass:'form-control' }}"""
    return field.as_widget(attrs={'class': css})
