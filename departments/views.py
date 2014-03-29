from django.views.generic import ListView, DetailView

from shifts.utils import group_shifts

from departments.models import Department


class DepartmentListView(ListView):
    model = Department


class DepartmentDetailView(DetailView):
    model = Department
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)
        context.update({
            'grouped_shifts': group_shifts(self.object.shifts.all()),
        })
        return context
