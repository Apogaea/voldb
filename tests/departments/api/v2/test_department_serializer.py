from volunteer.apps.departments.api.v2.serializers import DepartmentSerializer


def test_department_serialization(factories, models):
    department = factories.DepartmentFactory()

    serializer = DepartmentSerializer(department)

    expected = {
        'id': department.pk,
        'name': department.name,
        'description': department.description,
    }
    assert serializer.data == expected
