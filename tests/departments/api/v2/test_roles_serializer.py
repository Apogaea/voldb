from volunteer.apps.departments.api.v2.serializers import RoleSerializer


def test_role_serialization(factories):
    role = factories.RoleFactory()
    serializer = RoleSerializer(role)

    data = serializer.data
    assert data['id'] == role.pk
