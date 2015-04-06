from betterforms.forms import BetterModelForm

from volunteer.apps.events.models import Event


class AdminEventForm(BetterModelForm):
    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'registration_open_at',
            'registration_close_at',
        )
