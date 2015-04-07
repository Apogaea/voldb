import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.tables import BootstrapTable

from volunteer.apps.departments.models import Department


class DepartmentTable(BootstrapTable):
    name = tables.LinkColumn(
        'admin:department-detail',
        kwargs={'pk': A('pk')},
    )

    class Meta(BootstrapTable.Meta):
        model = Department
        fields = (
            'id',
            'name',
            # TODO:
        )
