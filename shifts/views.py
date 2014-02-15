from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from shifts.models import Shift
from departments.models import Department


# Create your views here.

def index(request):
    department_list = Department.objects.order_by('name').values('name','id')
    depts = ""
    for dept in department_list:
        dname = dept["name"]
        shift_list += {dept["name"],  Shift.objects.order_by('department', 'start_time').filter(department=dept["id"])}
    return render(request, 'shifts/index.html', {'shift_list': shift_list, 'department_list' : department_list})    
