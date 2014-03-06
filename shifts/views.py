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
        days = Shift.objects.order_by('start_time').values('start_time').distinct().datetimes("start_time", "day", tzinfo=None)
        shift_lengths = Shift.objects.values('shift_length').distinct()
        departments = Department.objects.order_by('name').values('name','id')
        shifts_lists = {}
        for day in days:
            t_month = day.date().strftime('%m')
            t_day = day.date().strftime('%d')
            t_year = day.date().strftime('%Y')
            t_date = day.date()
            shifts_lists[t_date] = {}
            for department in departments:
                shifts_lists[t_date][department['name']] = {}
                shifts_found_in_department = False
                for shift_length in shift_lengths:
                    shifts_lists[t_date][department['name']][shift_length['shift_length']] = {}
                    skip_blanks = 0
                    for t_hour in range(24):
                        if skip_blanks > 0:
                            skip_blanks -= 1 
                        else:
                            shifts_lists[t_date][department['name']][shift_length['shift_length']][t_hour] = {}
                        t_shifts = Shift.objects.filter(department=department['id'], shift_length=shift_length['shift_length'], start_time__year=t_year, start_time__month=t_month, start_time__day=t_day, start_time__hour=t_hour).order_by('start_time')
                        if t_shifts.__len__() > 0:
                            shifts_lists[t_date][department['name']][shift_length['shift_length']][t_hour] = t_shifts
                            shifts_found_in_department = True
                            skip_blanks = shift_length['shift_length']-1
                #while we want empty hours to loop through for rendering, we don't want to show empty departments
                if not shifts_found_in_department:
                    del shifts_lists[t_date][department['name']]

                        
#        pprint.pprint()

#        context['department'] = departments
#        context['shift_days'] = days
#        shift_lists = []
#        for department in departments:
#            shifts = {}
#            shifts['department'] = department['name']
#            shifts['shifts'] = Shift.objects.filter(department = department['id'], start_time__year='2014', start_time__month='6', start_time__day='3').order_by('shift_length', 'department', 'start_time')
#            shift_lists.append(shifts);
        context['shifts_lists'] = shifts_lists;        
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()
