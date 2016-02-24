from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import get_object_or_404

from authtools.views import LoginRequiredMixin

from volunteer.apps.events.utils import get_active_event

from volunteer.apps.shifts.export import (
    ShiftSlotReportView,
)

from volunteer.apps.departments.models import Department


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    context_object_name = 'departments'

    def get_queryset(self):
        active_event = get_active_event(self.request.session)
        return Department.objects.filter_to_active_event(active_event)

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        active_event = get_active_event(self.request.session)
        context['department_data'] = tuple((
            (
                department,
                {
                    'total_filled_shift_slots': department.total_filled_shift_slots(active_event),  # NOQA
                    'total_shift_slots': department.total_shift_slots(active_event),
                },
            ) for department in self.object_list
        ))
        return context


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'

    def get_queryset(self):
        active_event = get_active_event(self.request.session)
        return Department.objects.filter_to_active_event(
            active_event,
        ).prefetch_related('roles')

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)

        active_event = get_active_event(self.request.session)
        roles = self.object.roles.filter_to_active_event(active_event)
        context['roles'] = roles
        context['role_data'] = tuple((
            (
                role,
                {
                    'total_filled_shift_slots': role.total_filled_shift_slots(active_event),  # NOQA
                    'total_shift_slots': role.total_shift_slots(active_event),
                },
            ) for role in roles
        ))
        context['roles_with_shifts'] = tuple(
            (role, role.shifts.filter_to_active_event(active_event))
            for role in roles
        )
        return context


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
        active_event = get_active_event(self.request.session)
        return get_object_or_404(
            Department.objects.filter_to_active_event(active_event),
            pk=self.kwargs['pk'],
        )

    def get_filename(self):
        return 'shift-report-for-department-{0}.csv'.format(self.kwargs['pk'])

    def get_extra_filters(self):
        return dict(
            shift__role__department__id=self.kwargs['pk'],
        )
