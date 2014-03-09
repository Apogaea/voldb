import factory
from departments.models import Department


class DepartmentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Department
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = 'DPW'
    description = 'Deparment of Public Works'
    active_lead = None
    active_liaison = None
