from django.views.generic import TemplateView
from django.conf import settings

from volunteer.apps.events.utils import get_active_event


class SiteIndexView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(SiteIndexView, self).get_context_data(**kwargs)
        context['current_event'] = get_active_event(self.request.session)
        context['support_email'] = settings.DEFAULT_FROM_EMAIL
        return context
