from django.views.generic import (
    ListView,
    DetailView,
)

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.decorators import AdminRequiredMixin

from volunteer.apps.profiles.models import Profile

from .tables import ProfileTable


class AdminUserListView(AdminRequiredMixin, SingleTableMixin, ListView):
    template_name = 'admin/accounts/user_list.html'
    context_object_name = 'profiles'
    model = Profile
    table_class = ProfileTable
    table_pagination = {'per_page': 20}

    def get_context_data(self, **kwargs):
        context = super(AdminUserListView, self).get_context_data(**kwargs)
        import ipdb; ipdb.set_trace()
        return context


class AdminUserDetailView(AdminRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'admin/accounts/user_detail.html'
