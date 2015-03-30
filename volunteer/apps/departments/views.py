from django.views.generic import ListView, DetailView

from authtools.views import LoginRequiredMixin

from volunteer.apps.departments.models import Department


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.filter(roles__isnull=False).distinct()


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'

    def get_queryset(self):
        return Department.objects.filter(
            roles__isnull=False,
        ).distinct().prefetch_related('roles')
