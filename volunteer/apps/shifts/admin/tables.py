import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.tables import BootstrapTable

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)


class ShiftTable(BootstrapTable):
    id = tables.LinkColumn(
        'admin:shift-detail',
        kwargs={
            'department_pk': A('role.department_id'),
            'role_pk': A('role_id'),
            'pk': A('pk'),
        },
    )
    end_time = tables.DateTimeColumn(
        verbose_name='shift ends',
        orderable=False,
    )
    duration = tables.Column(
        orderable=False,
    )

    class Meta(BootstrapTable.Meta):
        model = Shift
        fields = (
            'id',
            'start_time',
            'end_time',
            'duration',
            'num_slots',
            'code',
        )


class ShiftSlotReportTable(BootstrapTable):
    slot_id = tables.Column(accessor=A('pk'))

    department_id = tables.Column(
        verbose_name="Department ID", accessor=A('shift.role.department_id'),
    )
    department_name = tables.Column(
        verbose_name="Department Name", accessor=A('shift.role.department'),
    )

    role_id = tables.Column(verbose_name="Role ID", accessor=A('shift.role_id'))
    role_name = tables.Column(verbose_name="Role name", accessor=A('shift.role'))

    shift_id = tables.Column(verbose_name="Shift ID", accessor=A('shift.pk'))
    shift_start_time = tables.Column(
        verbose_name="Shift Start Time", accessor=A('shift.start_time'),
    )
    shift_end_time = tables.Column(
        verbose_name="Shift End Time", accessor=A('shift.end_time'),
    )

    volunteer_id = tables.Column(
        verbose_name="Volunteer ID", accessor=A('volunteer.pk'),
    )
    volunteer_display_name = tables.Column(
        verbose_name="Volunteer Display Name", accessor=A('volunteer.profile.display_name'),
    )
    volunteer_full_name = tables.Column(
        verbose_name="Volunteer Full Name", accessor=A('volunteer.profile.full_name'),
    )
    volunteer_phone_number = tables.Column(
        verbose_name="Volunteer Phone Number", accessor=A('volunteer.profile.phone'),
    )
    volunteer_email = tables.Column(
        verbose_name="Volunteer Email", accessor=A('volunteer.email'),
    )

    class Meta(BootstrapTable.Meta):
        model = ShiftSlot
        fields = (
            'slot_id',
            'department_id',
            'department_name',
            'role_id',
            'role_name',
            'shift_id',
            'shift_start_time',
            'shift_end_time',
            'volunteer_id',
            'volunteer_display_name',
            'volunteer_full_name',
            'volunteer_phone_number',
            'volunteer_email',
        )
