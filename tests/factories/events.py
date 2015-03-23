import factory

from django.utils import timezone

from volunteer.apps.events.models import (
    Event,
)


class EventFactory(factory.DjangoModelFactory):
    name = 'Apogaea'

    registration_open_at = factory.LazyAttribute(
        lambda e: timezone.now() - timezone.timedelta(10)
    )
    registration_close_at = factory.LazyAttribute(
        lambda e: timezone.now() + timezone.timedelta(10)
    )

    class Meta:
        model = Event
