from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from departments.models import Department
# Create your views here.


def index(request):
    department_list = Department.objects.all()	
    return render(request, 'departments/index.html', {'department_list': department_list})

@login_required
def detail(request, department_id):
    return HttpResponse("You're looking at department %s." % department_id)    