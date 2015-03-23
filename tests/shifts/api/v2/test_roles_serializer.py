from volunteer.apps.shifts.api.v2.serializers import RoleSerializer


def test_role_serialization_with_no_shifts(factories):
    role = factories.RoleFactory()
    serializer = RoleSerializer(role)

    data = serializer.data
    assert data['shifts'] == []


def test_role_serialization_with_shifts(factories):
    role = factories.RoleFactory()
    factories.ShiftFactory.create_batch(3, role=role)
    serializer = RoleSerializer(role)

    data = serializer.data
    assert len(data['shifts']) == 3
