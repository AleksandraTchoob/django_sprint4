from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.
class AboutView(TemplateView):
    """Страница 'О проекте'."""
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Страница 'Правила'."""
    template_name = 'pages/rules.html'


def csrf_failure(request, reason=""):
    """Кастомная страница ошибки CSRF 403."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """Кастомная страница ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Кастомная страница ошибки 500."""
    return render(request, 'pages/500.html', status=500)
