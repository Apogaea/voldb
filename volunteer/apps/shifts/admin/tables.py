import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.tables import BootstrapTable

from volunteer.apps.shifts.models import (
    Shift,
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
