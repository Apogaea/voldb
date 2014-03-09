from django.views.generic import TemplateView, DetailView
from shifts.models import Shift
from departments.models import Department
import pprint
import time


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


#shift this have been a list view? should I be using group by?
class GridView(TemplateView):
    department_list = Department.objects.order_by('name').values('name', 'id')
    template_name = "shifts/shifts.html"

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)

        shifts = Shift.object.order_by(
            'start_time__year',
            'start_time__month',
            'start_time__day',
            'department',
            'shift_length',
            'start_time__hour',
            'start_time__minute',
            'start_time__second'
        )

        #we want to group by department, thenday, day, then shift length
        days = Shift.objects.order_by('start_time').values('start_time').distinct().datetimes("start_time", "day", tzinfo=None)
        shift_lengths = Shift.objects.values('shift_length').distinct()
        departments = Department.objects.order_by('name').values('name', 'id')

        #for each day, we build a dictionary of departments

        context['shifts_lists'] = shifts_lists
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()
