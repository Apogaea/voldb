import unicodecsv as csv

from django.shortcuts import (
    get_object_or_404,
)
from django.core.urlresolvers import (
    reverse,
    reverse_lazy,
)
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
)
from django.http import HttpResponse

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.decorators import AdminRequiredMixin

from volunteer.apps.shifts.export import (
    CSV_HEADERS,
    shift_slot_to_csv_row,
)
from volunteer.apps.shifts.admin.tables import (
    ShiftTable,
    ShiftSlotReportTable,
)
from volunteer.apps.shifts.models import (
    ShiftSlot,
)

from volunteer.apps.departments.models import (
    Department,
    Role,
)

from .tables import (
    DepartmentTable,
    RoleTable,
)
from .forms import (
    AdminDepartmentForm,
    AdminDepartmentMergeForm,
    AdminRoleForm,
    AdminRoleMergeForm,
)


class ShiftSlotReportView(SingleTableMixin, ListView):
    context_object_name = 'shifts'
    model = ShiftSlot
    table_class = ShiftSlotReportTable

    def return_csv_download(self, *args, **kwargs):
        filename = 'shift-report-for-role-{0}.csv'.format(self.kwargs['pk'])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

        writer = csv.DictWriter(response, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for shift_slot in self.get_queryset():
            row = shift_slot_to_csv_row(shift_slot)
            writer.writerow(row)
        return response

    def get(self, *args, **kwargs):
        if 'download' in self.request.GET:
            return self.return_csv_download(*args, **kwargs)
        else:
            return super(ShiftSlotReportView, self).get(*args, **kwargs)

    def get_extra_filters(self):
        raise NotImplementedError("Must be implemented by subclass")

    def get_queryset(self):
        return ShiftSlot.objects.filter(
            cancelled_at__isnull=True,
            **self.get_extra_filters()
        ).filter_to_current_event(
        ).order_by(
            'shift__role__department',
            'shift__role',
            'shift__start_time',
            'shift__shift_minutes',
            'volunteer___profile__display_name',
        ).select_related()


class AdminRoleShiftSlotReportView(AdminRequiredMixin, ShiftSlotReportView):
    template_name = 'admin/departments/role_shift_slot_report.html'

    def get_context_data(self, **kwargs):
        context = super(AdminRoleShiftSlotReportView, self).get_context_data(**kwargs)
        context['role'] = self.get_role()
        return context

    def get_role(self):
        return get_object_or_404(
            Role.objects.filter(department_id=self.kwargs['department_pk']),
            pk=self.kwargs['pk'],
        )

    def get_extra_filters(self):
        return dict(
            shift__role__id=self.kwargs['pk'],
            shift__role__department__id=self.kwargs['department_pk'],
        )


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


class AdminDepartmentDetailView(AdminRequiredMixin, SingleTableMixin, UpdateView):
    model = Department
    template_name = 'admin/departments/department_detail.html'
    form_class = AdminDepartmentForm
    table_class = RoleTable

    def get_table_data(self):
        return self.object.roles.all()

    def get_success_url(self):
        return reverse('admin:department-detail', kwargs=self.kwargs)


class AdminDepartmentMergeView(AdminRequiredMixin, UpdateView):
    model = Department
    template_name = 'admin/departments/department_merge.html'
    form_class = AdminDepartmentMergeForm

    def get_success_url(self):
        return reverse('admin:department-detail', kwargs={'pk': self.object.pk})


class AdminRoleCreateView(AdminRequiredMixin, CreateView):
    model = Role
    template_name = 'admin/departments/role_create.html'
    form_class = AdminRoleForm

    def get_context_data(self, **kwargs):
        context = super(AdminRoleCreateView, self).get_context_data(**kwargs)
        context['department'] = Department.objects.get(pk=self.kwargs['department_pk'])
        return context

    def form_valid(self, form):
        form.instance.department_id = self.kwargs['department_pk']
        return super(AdminRoleCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'admin:department-detail',
            kwargs={'pk': self.object.department_id},
        )


class AdminRoleDetailView(AdminRequiredMixin, SingleTableMixin, UpdateView):
    model = Role
    template_name = 'admin/departments/role_detail.html'
    form_class = AdminRoleForm
    table_class = ShiftTable

    def get_queryset(self):
        return Role.objects.filter(department_id=self.kwargs['department_pk'])

    def get_table_data(self):
        return self.object.shifts.filter_to_current_event().order_by(
            'start_time', 'shift_minutes',
        )

    def get_success_url(self):
        return reverse(
            'admin:department-detail',
            kwargs={'pk': self.object.department_id},
        )


class AdminRoleMergeView(AdminRequiredMixin, UpdateView):
    model = Role
    template_name = 'admin/departments/role_merge.html'
    form_class = AdminRoleMergeForm

    def get_queryset(self):
        return Role.objects.filter(department_id=self.kwargs['department_pk'])

    def get_success_url(self):
        return reverse(
            'admin:role-detail',
            kwargs={
                'department_pk': self.object.department_id,
                'pk': self.object.pk,
            },
        )
