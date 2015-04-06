from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
)

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.decorators import AdminRequiredMixin

from volunteer.apps.events.models import Event

from .tables import EventTable
from .forms import AdminEventForm


class AdminEventListView(AdminRequiredMixin, SingleTableMixin, ListView):
    template_name = 'admin/events/event_list.html'
    context_object_name = 'events'
    model = Event
    table_class = EventTable
    table_pagination = {'per_page': 20}


class AdminEventCreateView(AdminRequiredMixin, CreateView):
    model = Event
    template_name = 'admin/events/event_create.html'
    form_class = AdminEventForm
    success_url = reverse_lazy('admin:event-list')
