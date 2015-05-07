from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import get_object_or_404

from authtools.views import LoginRequiredMixin

from volunteer.apps.shifts.export import (
    ShiftSlotReportView,
)

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


class DepartmentShiftSlotReportView(LoginRequiredMixin, ShiftSlotReportView):
    template_name = 'departments/department_lead_shift_slot_report.html'

    def dispatch(self, *args, **kwargs):
        department = self.get_department()
        if not department.user_can_admin(self.request.user):
            raise Http404
        return super(DepartmentShiftSlotReportView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DepartmentShiftSlotReportView, self).get_context_data(
            **kwargs
        )
        context['department'] = self.get_department()
        return context

    def get_department(self):
        return get_object_or_404(
            Department.objects.filter_to_current_event(),
            pk=self.kwargs['pk'],
        )

    def get_filename(self):
        return 'shift-report-for-department-{0}.csv'.format(self.kwargs['pk'])

    def get_extra_filters(self):
        return dict(
            shift__role__department__id=self.kwargs['pk'],
        )
