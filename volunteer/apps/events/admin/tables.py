import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.tables import BootstrapTable

from volunteer.apps.events.models import Event


class EventTable(BootstrapTable):
    name = tables.LinkColumn(
        'admin:event-detail',
        kwargs={'pk': A('pk')},
    )
    is_current = tables.BooleanColumn(
        orderable=False,
    )
    is_registration_open = tables.BooleanColumn(
        orderable=False,
    )

    class Meta(BootstrapTable.Meta):
        model = Event
        fields = (
            'id',
            'name',
            'is_current',
            'is_registration_open',
            'registration_open_at',
            'registration_close_at',
        )
