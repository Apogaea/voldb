import factory

from volunteer.apps.departments.models import Department


class DepartmentFactory(factory.DjangoModelFactory):
    name = 'DPW'
    description = 'Department of Public Works'
    active_lead = None
    active_liaison = None

    class Meta:
        model = Department
        django_get_or_create = ('name',)
