from django.views.generic import ListView, DetailView

from authtools.views import LoginRequiredMixin

from volunteer.apps.departments.models import Department


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.filter_to_current_event()


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'

    def get_queryset(self):
        return Department.objects.filter_to_current_event().prefetch_related('roles')
