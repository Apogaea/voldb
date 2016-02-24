from django.shortcuts import (
    get_object_or_404,
    redirect,
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

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.decorators import (
    AdminRequiredMixin,
)

from volunteer.apps.events.utils import get_active_event

from volunteer.apps.shifts.export import (
    ShiftSlotReportView,
)
from volunteer.apps.shifts.admin.tables import (
    ShiftTable,
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
    AdminDepartmentAddLeadForm,
    AdminDepartmentRemoveLeadForm,
    AdminRoleForm,
    AdminRoleMergeForm,
)


class AdminDepartmentListView(AdminRequiredMixin, SingleTableMixin, ListView):
    template_name = 'admin/departments/department_list.html'
    context_object_name = 'departments'
    model = Department
    table_class = DepartmentTable
    table_pagination = {'per_page': 20}

    def get_queryset(self):
        return super(AdminDepartmentListView, self).get_queryset().prefetch_related('leads')


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


class AdminDepartmentAddLead(AdminRequiredMixin, UpdateView):
    model = Department
    context_object_name = 'department'
    form_class = AdminDepartmentAddLeadForm
    template_name = 'admin/departments/department_add_lead.html'

    def form_valid(self, form):
        form.instance.leads.add(form.cleaned_data['user'])
        return redirect(reverse('admin:department-detail', kwargs=self.kwargs))


class AdminDepartmentRemoveLead(AdminRequiredMixin, UpdateView):
    model = Department
    context_object_name = 'department'
    form_class = AdminDepartmentRemoveLeadForm
    template_name = 'admin/departments/department_remove_lead.html'

    def dispatch(self, *args, **kwargs):
        if not self.get_object().leads.filter(pk=self.kwargs['lead_pk']).exists():
            return redirect(
                'admin:department-detail',
                kwargs={'pk': self.kwargs['pk']},
            )
        return super(AdminDepartmentRemoveLead, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminDepartmentRemoveLead, self).get_context_data(
            **kwargs
        )
        context['lead'] = self.get_lead()
        return context

    def get_lead(self):
        return get_object_or_404(
            self.object.leads.all(),
            pk=self.kwargs['lead_pk'],
        )

    def form_valid(self, form):
        form.instance.leads.remove(self.get_lead())
        return redirect(
            reverse('admin:department-detail', kwargs={'pk': self.kwargs['pk']}),
        )


class AdminDepartmentShiftSlotReportView(AdminRequiredMixin, ShiftSlotReportView):
    template_name = 'admin/departments/department_shift_slot_report.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDepartmentShiftSlotReportView, self).get_context_data(**kwargs)
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
        active_event = get_active_event(self.request.session)
        return self.object.shifts.filter_to_active_event(active_event).order_by(
            'start_time', 'shift_minutes',
        )

    def get_success_url(self):
        return reverse(
            'admin:department-detail',
            kwargs={'pk': self.object.department_id},
        )


class AdminRoleShiftSlotReportView(AdminRequiredMixin, ShiftSlotReportView):
    template_name = 'admin/departments/role_shift_slot_report.html'

    def get_context_data(self, **kwargs):
        context = super(AdminRoleShiftSlotReportView, self).get_context_data(**kwargs)
        context['role'] = self.get_role()
        return context

    def get_role(self):
        active_event = get_active_event(self.request.session)
        return get_object_or_404(
            Role.objects.filter(
                department_id=self.kwargs['department_pk'],
            ).filter_to_active_event(active_event),
            pk=self.kwargs['pk'],
        )

    def get_extra_filters(self):
        return dict(
            shift__role__id=self.kwargs['pk'],
            shift__role__department__id=self.kwargs['department_pk'],
        )

    def get_filename(self):
        return 'shift-report-for-role-{0}.csv'.format(self.kwargs['pk'])


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
