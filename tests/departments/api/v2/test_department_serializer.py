from volunteer.apps.departments.api.v2.serializers import DepartmentSerializer


def test_department_serialization(factories, models):
    liaison = factories.UserFactory()
    lead = factories.UserFactory()
    department = factories.DepartmentFactory(
        active_liaison=liaison,
        active_lead=lead,
    )

    serializer = DepartmentSerializer(department)

    expected = {
        'id': department.pk,
        'name': department.name,
        'description': department.description,
        'liaison': [liaison.pk],
        'lead': lead.pk,
    }
    assert serializer.data == expected
