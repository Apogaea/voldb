from django.core.urlresolvers import (
    reverse,
    reverse_lazy,
)
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
)

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.decorators import AdminRequiredMixin

from volunteer.apps.departments.models import Department

from .tables import DepartmentTable
from .forms import AdminDepartmentForm


class AdminDepartmentListView(AdminRequiredMixin, SingleTableMixin, ListView):
    template_name = 'admin/departments/department_list.html'
    context_object_name = 'departments'
    model = Department
    table_class = DepartmentTable
    table_pagination = {'per_page': 20}


class AdminDepartmentCreateView(AdminRequiredMixin, CreateView):
    model = Department
    template_name = 'admin/departments/department_create.html'
    form_class = AdminDepartmentForm
    success_url = reverse_lazy('admin:department-list')


class AdminDepartmentDetailView(AdminRequiredMixin, UpdateView):
    model = Department
    template_name = 'admin/departments/department_detail.html'
    form_class = AdminDepartmentForm

    def get_success_url(self):
        return reverse('admin:department-detail', kwargs=self.kwargs)
