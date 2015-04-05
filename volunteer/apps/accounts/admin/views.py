from django.views.generic import (
    ListView,
)

from volunteer.decorators import AdminRequiredMixin


class AdminUserListView(AdminRequiredMixin, ListView):
    template_name = 'admin/accounts/user_list.html'
