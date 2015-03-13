from django.views.generic import TemplateView


class SiteIndexView(TemplateView):
    template_name = 'home.html'
