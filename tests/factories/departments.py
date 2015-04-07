import factory

from volunteer.apps.departments.models import (
    Department,
    Role,
)


class DepartmentFactory(factory.DjangoModelFactory):
    name = 'DPW'
    description = 'Department of Public Works'
    active_lead = None
    active_liaison = None

    class Meta:
        model = Department
        django_get_or_create = ('name',)


class RoleFactory(factory.DjangoModelFactory):
    name = factory.Sequence("role-{0}".format)
    description = "Role Description"
    department = factory.SubFactory('tests.factories.departments.DepartmentFactory')

    class Meta:
        model = Role
