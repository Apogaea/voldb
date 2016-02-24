from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from volunteer.apps.events.models import Event

from .serializers import ActiveEventSerializer


class EventViewSet(viewsets.GenericViewSet):
    queryset = Event.objects.none()
    serializer_class = ActiveEventSerializer

    @list_route(methods=['post'])
    def select_active(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        active_event = serializer.validated_data['active_event']
        self.request.session.set('event_id', active_event.pk)

        return Response(status=status.HTTP_204_NO_CONTENT)
