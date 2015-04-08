from django.shortcuts import get_object_or_404
from django.core.urlresolvers import (
    reverse,
)
from django.views.generic import (
    UpdateView,
    CreateView,
)

from volunteer.decorators import AdminRequiredMixin

from volunteer.apps.events.models import Event

from volunteer.apps.departments.models import Role

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)

from .forms import (
    AdminShiftCreateForm,
    AdminShiftUpdateForm,
    AdminShiftSlotCancelForm,
)


class AdminShiftCreateView(AdminRequiredMixin, CreateView):
    model = Shift
    template_name = 'admin/shifts/shift_create.html'
    form_class = AdminShiftCreateForm
    context_object_name = 'shift'

    def get_context_data(self, **kwargs):
        context = super(AdminShiftCreateView, self).get_context_data(**kwargs)
        context['role'] = Role.objects.get(
            department_id=self.kwargs['department_pk'],
            id=self.kwargs['role_pk'],
        )
        return context

    def form_valid(self, form):
        form.instance.role_id = self.kwargs['role_pk']
        form.instance.event = Event.objects.get_current()
        return super(AdminShiftCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'admin:role-detail',
            kwargs={
                'department_pk': self.object.role.department_id,
                'pk': self.object.role_id,
            },
        )


class AdminShiftDetailView(AdminRequiredMixin, UpdateView):
    model = Shift
    template_name = 'admin/shifts/shift_detail.html'
    form_class = AdminShiftUpdateForm
    context_object_name = 'shift'

    def get_queryset(self):
        return Shift.objects.filter(
            role__department_id=self.kwargs['department_pk'],
            role_id=self.kwargs['role_pk'],
        ).filter_to_current_event()

    def get_success_url(self):
        return reverse(
            'admin:shift-detail',
            kwargs=self.kwargs,
        )


class AdminShiftSlotCancelView(AdminRequiredMixin, UpdateView):
    model = ShiftSlot
    template_name = 'admin/shifts/shift_slot_cancel.html'
    form_class = AdminShiftSlotCancelForm
    context_object_name = 'shift_slot'

    def get_queryset(self):
        shift = get_object_or_404(
            Shift.objects.filter_to_current_event(),
            role__department_id=self.kwargs['department_pk'],
            role_id=self.kwargs['role_pk'],
            pk=self.kwargs['shift_pk'],
        )
        return shift.slots.all()

    def get_success_url(self):
        return reverse(
            'admin:shift-detail',
            kwargs={
                'department_pk': self.kwargs['department_pk'],
                'role_pk': self.kwargs['role_pk'],
                'pk': self.kwargs['shift_pk'],
            },
        )
