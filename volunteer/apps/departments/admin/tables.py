import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.tables import BootstrapTable

from volunteer.apps.departments.models import (
    Department,
    Role,
)


class DepartmentTable(BootstrapTable):
    id = tables.LinkColumn(
        'admin:department-detail',
        kwargs={'pk': A('pk')},
    )
    name = tables.LinkColumn(
        'admin:department-detail',
        kwargs={'pk': A('pk')},
    )

    class Meta(BootstrapTable.Meta):
        model = Department
        fields = (
            'id',
            'name',
        )


class RoleTable(BootstrapTable):
    id = tables.LinkColumn(
        'admin:role-detail',
        kwargs={
            'pk': A('pk'),
            'department_pk': A('department_id'),
        },
    )
    name = tables.LinkColumn(
        'admin:role-detail',
        kwargs={
            'pk': A('pk'),
            'department_pk': A('department_id'),
        },
    )

    class Meta(BootstrapTable.Meta):
        model = Role
        fields = (
            'id',
            'name',
            'description',
        )
