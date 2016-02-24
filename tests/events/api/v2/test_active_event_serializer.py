import pytest


@pytest.fixture()
def ActiveEventSerializer(db):
    """
    Importing this class triggers a db query so lets be sure the database is
    setup before hand.
    """
    from volunteer.apps.events.api.v2.serializers import (
        ActiveEventSerializer as _ActiveEventSerializer,
    )
    return _ActiveEventSerializer


@pytest.mark.django_db
def test_allows_null(ActiveEventSerializer):
    data = {'active_event': None}

    serializer = ActiveEventSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['active_event'] is None


def test_selecting_event(factories, ActiveEventSerializer):
    factories.FutureEventFactory(name='A')
    event_b = factories.PastEventFactory(name='B')

    data = {'active_event': str(event_b.pk)}

    serializer = ActiveEventSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['active_event'] == str(event_b.pk)


def test_validates_selection(factories, ActiveEventSerializer):
    data = {'active_event': 1234567890}

    serializer = ActiveEventSerializer(data=data)
    assert not serializer.is_valid()
