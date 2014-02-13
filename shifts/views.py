from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from shifts.models import Shift


# Create your views here.

def index(request):
    shift_list = Shift.objects.all()  
    return render(request, 'shifts/index.html', {'shift_list': shift_list})    
