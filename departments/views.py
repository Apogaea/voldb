from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
# Create your views here.
	
@login_required
def index(request):
    template = loader.get_template('departments/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def detail(request, department_id):
    return HttpResponse("You're looking at department %s." % department_id)    