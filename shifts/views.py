from django.views.generic import TemplateView, DetailView, ListView
from departments.models import Department
from shifts.models import Shift
from shifts.utils import group_shifts, shifts_to_tabular_data


class ClaimView(DetailView):
    queryset = Shift.objects.all()
    template_name = "shifts/shift.html"

    def get_object(self):
        #to fake some server latency
        #time.sleep(2)
        # Call the superclass
        shift = super(ClaimView, self).get_object()
        # Update the user
        shift.owner = self.request.user
        shift.save()
        return shift


class ReleaseView(DetailView):
    queryset = Shift.objects.all()
    template_name = "shifts/shift.html"

    def get_object(self):
        # Call the superclass
        shift = super(ReleaseView, self).get_object()
        # Record the last accessed date
        if shift.owner == self.request.user:
            shift.owner = None
            shift.save()
        # Return the object
        return shift


class GridView(ListView):
    template_name = "shifts/shifts.html"
    model = Shift

    def get_queryset(self):
        qs = super(GridView, self).get_queryset()
        return qs.select_related()

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)

        context['grouped_shifts'] = list(group_shifts(self.object_list))
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()
