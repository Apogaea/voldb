from rest_framework import serializers
from rest_framework.fields import (
    to_choices_dict,
    flatten_choices_dict,
)

from volunteer.apps.events.models import Event


class EventChoiceField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(EventChoiceField, self).__init__([], *args, **kwargs)

    @property
    def grouped_choices(self):
        return to_choices_dict(Event.get_event_choices())

    @grouped_choices.setter
    def grouped_choices(self, value):
        pass

    @property
    def choices(self):
        return flatten_choices_dict(self.grouped_choices)

    @choices.setter
    def choices(self, value):
        pass


class ActiveEventSerializer(serializers.Serializer):
    active_event = EventChoiceField(allow_null=True)
