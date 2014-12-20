from django.views.generic import ListView, DetailView

from authtools.views import LoginRequiredMixin

from departments.models import Department


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'
