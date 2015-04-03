from django.views.generic import TemplateView

from volunteer.decorators import AdminRequiredMixin


class AdminIndexView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/index.html'


class AdminLoginView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/login.html'
