from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.core.urlresolvers import (
    reverse,
)
from django.views.generic import (
    UpdateView,
    CreateView,
    DeleteView,
)

from volunteer.decorators import AdminRequiredMixin

from volunteer.apps.events.models import Event

from volunteer.apps.departments.models import (
    Role,
)

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)

from .forms import (
    AdminShiftCreateForm,
    AdminShiftUpdateForm,
    AdminShiftSlotCancelForm,
    AdminShiftSlotCreateForm,
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


class AdminShiftDeleteView(AdminRequiredMixin, DeleteView):
    model = Shift
    template_name = 'admin/shifts/shift_delete.html'
    context_object_name = 'shift'

    def get_queryset(self):
        return Shift.objects.filter(
            role__department_id=self.kwargs['department_pk'],
            role_id=self.kwargs['role_pk'],
        ).filter_to_current_event()

    def delete(self, *args, **kwargs):
        if self.get_object().claimed_slots.exists():
            messages.info(self.request, (
                'You must remove all volunteers from this shift prior to deletion'
            ))
            return self.get(*args, **kwargs)
        return super(AdminShiftDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self):
        return reverse(
            'admin:role-detail',
            kwargs={
                'department_pk': self.kwargs['department_pk'],
                'pk': self.kwargs['role_pk'],
            },
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


class AdminShiftSlotCreateView(AdminRequiredMixin, CreateView):
    model = ShiftSlot
    template_name = 'admin/shifts/shift_slot_create.html'
    form_class = AdminShiftSlotCreateForm

    def get_context_data(self, **kwargs):
        context = super(AdminShiftSlotCreateView, self).get_context_data(**kwargs)
        context['shift'] = self.get_shift()
        return context

    def get_shift(self):
        return get_object_or_404(
            Shift.objects.filter_to_current_event(),
            role__department_id=self.kwargs['department_pk'],
            role_id=self.kwargs['role_pk'],
            pk=self.kwargs['pk'],
        )

    def form_valid(self, form):
        shift_slot = form.instance
        shift_slot.shift = self.get_shift()
        shift_slot.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(AdminShiftSlotCreateView, self).get_form_kwargs()
        kwargs['shift'] = self.get_shift()
        return kwargs

    def get_success_url(self):
        return reverse(
            'admin:shift-detail',
            kwargs={
                'department_pk': self.kwargs['department_pk'],
                'role_pk': self.kwargs['role_pk'],
                'pk': self.kwargs['pk'],
            },
        )
