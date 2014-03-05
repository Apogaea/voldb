from django.views.generic import TemplateView
from shifts.models import Shift
from departments.models import Department
from datetime import date,datetime
import pprint

# Create your views here.
class GridView(TemplateView):
    department_list = Department.objects.order_by('name').values('name','id')
    template_name = "shifts/shifts.html"    

    def get_context_data(self, **kwargs):   
        context = super(GridView, self).get_context_data(**kwargs)

        #we want to group by department, thenday, day, then shift length
        days = Shift.objects.values('start_time').distinct().datetimes("start_time", "day", tzinfo=None)
        shift_lengths = Shift.objects.values('shift_length').distinct()
        departments = Department.objects.order_by('name').values('name','id')
        shift_lists = {}
        for department in departments:
            shift_lists[department['name']] = {}
            for day in days:
                t_month = day.date().strftime('%m')
                t_day = day.date().strftime('%d')
                t_year = day.date().strftime('%Y')
                t_date = day.date().strftime('%Y-%m-%d')                
                shift_lists[department['name']][t_date] = {}
                for shift_length in shift_lengths:
                    t_shifts = Shift.objects.filter(department=department['id'], shift_length=shift_length['shift_length'], start_time__year=t_year, start_time__month=t_month, start_time__day=t_day).order_by('start_time')
                    if t_shifts.__len__() > 0:            
                        shift_lists[department['name']][t_date][shift_length['shift_length']] = t_shifts

                        
        pprint.pprint(shift_lists)

        context['department_list'] = departments
#        context['shift_days'] = days
#        shift_lists = []
#        for department in departments:
#            shifts = {}
#            shifts['department'] = department['name']
#            shifts['shifts'] = Shift.objects.filter(department = department['id'], start_time__year='2014', start_time__month='6', start_time__day='3').order_by('shift_length', 'department', 'start_time')
#            shift_lists.append(shifts);
        context['shift_lists'] = shift_lists;        
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()
