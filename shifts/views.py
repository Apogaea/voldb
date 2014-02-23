from django.views.generic import TemplateView
from shifts.models import Shift
from departments.models import Department

# Create your views here.
class GridView(TemplateView):
    department_list = Department.objects.order_by('name').values('name','id')
    template_name = "shifts/shifts.html"    
  #  return render(request, 'shifts/shifts.html', {'shift_list': shift_list, 'department_list' : department_list})    
    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)
        departments = Department.objects.order_by('name').values('name','id')
        context['department_list'] = departments
        shift_lists = []
        for department in departments:
            shifts = {}
            shifts['department'] = department['name']
            shifts['shifts'] = Shift.objects.filter(department = department['id']).order_by('department', 'start_time').values('name','id')
            shift_lists.append(shifts);
        context['shift_lists'] = shift_lists;
        return context


#def index(request):
#    department_list = Department.objects.order_by('name').values('name','id')
#    shift_list = Shift.objects.order_by('department', 'start_time')
#    return render(request, 'shifts/shifts.html', {'shift_list': shift_list, 'department_list' : department_list})    
