from django.db.models import Q
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
from .forms import (
    AdminUserChangeForm,
    AdminUserSearchForm,
)


User = get_user_model()


class AdminUserListView(AdminRequiredMixin, SingleTableMixin, ListView):
    template_name = 'admin/accounts/user_list.html'
    context_object_name = 'users'
    model = User
    table_class = UserTable
    table_pagination = {'per_page': 20}

    def get_queryset(self):
        qs = super(AdminUserListView, self).get_queryset()
        form = AdminUserSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get('q'):
            q = form.cleaned_data['q']
            return qs.filter(
                Q(email__icontains=q) |
                Q(_profile__full_name__icontains=q) |
                Q(_profile__display_name__icontains=q)
            )
        return qs


class AdminUserDetailView(AdminRequiredMixin, UpdateView):
    model = User
    context_object_name = 'voldb_user'
    template_name = 'admin/accounts/user_detail.html'
    form_class = AdminUserChangeForm

    def get_success_url(self):
        return reverse('admin:user-detail', kwargs=self.kwargs)
