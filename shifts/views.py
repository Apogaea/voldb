from django.views.generic import TemplateView, DetailView
from shifts.models import Shift
from departments.models import Department
from datetime import date,datetime
import pprint
import time

# Create your views here.
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
    department_list = Department.objects.order_by('name').values('name','id')
    template_name = "shifts/shifts.html"    

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)

        #we want to group by department, thenday, day, then shift length
        days = Shift.objects.order_by('start_time').values('start_time').distinct().datetimes("start_time", "day", tzinfo=None)
        shift_lengths = Shift.objects.values('shift_length').distinct()
        departments = Department.objects.order_by('name').values('name','id')

        #for each day, we build a dictionary of departments
        shifts_lists = {}
        for day in days:
            t_month = day.date().strftime('%m')
            t_day = day.date().strftime('%d')
            t_year = day.date().strftime('%Y')
            t_date = day.date()
            shifts_lists[t_date] = {}
            #for each department, we build a dictionary indexed by shift lengths
            for department in departments:
                shifts_lists[t_date][department['name']] = {}
                shifts_found_in_department = False
                #for each set of shifts lengths, we build a per-hour list of shifts
                for shift_length in shift_lengths:
                    #for easier render, we fill in blank hours
                    shifts_lists[t_date][department['name']][shift_length['shift_length']] = {}
                    skip_blanks = 0
                    for t_hour in range(24):
                        if skip_blanks > 0:
                            skip_blanks -= 1 
                        else:
                            shifts_lists[t_date][department['name']][shift_length['shift_length']][t_hour] = {}

                        t_shifts = Shift.objects.filter(department=department['id'], 
                                                        shift_length=shift_length['shift_length'], 
                                                        start_time__year=t_year, 
                                                        start_time__month=t_month, 
                                                        start_time__day=t_day, 
                                                        start_time__hour=t_hour).order_by('start_time').select_related('owner','id')
                        if t_shifts.__len__() > 0:
                            shifts_lists[t_date][department['name']][shift_length['shift_length']][t_hour] = t_shifts
                            shifts_found_in_department = True
                            skip_blanks = shift_length['shift_length']-1
                #while we want empty hours to loop through for rendering, we don't want to show empty departments
                if not shifts_found_in_department:
                    del shifts_lists[t_date][department['name']]
                        
        pprint.pprint(shifts_lists)

        context['shifts_lists'] = shifts_lists;        
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()
