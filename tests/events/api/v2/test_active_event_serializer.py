import pytest

from volunteer.apps.events.api.v2.serializers import ActiveEventSerializer


@pytest.mark.django_db
def test_allows_null():
    data = {'active_event': None}

    serializer = ActiveEventSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['active_event'] is None


def test_selecting_event(factories):
    factories.FutureEventFactory(name='A')
    event_b = factories.PastEventFactory(name='B')

    data = {'active_event': str(event_b.pk)}

    serializer = ActiveEventSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['active_event'] == str(event_b.pk)


def test_validates_selection(factories):
    data = {'active_event': 1234567890}

    serializer = ActiveEventSerializer(data=data)
    assert not serializer.is_valid()
