from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    UpdateView,
)

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.decorators import AdminRequiredMixin

from .tables import UserTable
from .forms import AdminUserChangeForm


User = get_user_model()


class AdminUserListView(AdminRequiredMixin, SingleTableMixin, ListView):
    template_name = 'admin/accounts/user_list.html'
    context_object_name = 'users'
    model = User
    table_class = UserTable
    table_pagination = {'per_page': 20}


class AdminUserDetailView(AdminRequiredMixin, UpdateView):
    model = User
    context_object_name = 'voldb_user'
    template_name = 'admin/accounts/user_detail.html'
    form_class = AdminUserChangeForm

    def get_success_url(self):
        return reverse('admin:user-detail', kwargs=self.kwargs)
