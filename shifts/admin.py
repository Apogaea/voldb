from django.contrib import admin
from shifts.models import Shift
# Register your models here.

class ShiftAdmin(admin.ModelAdmin):
	list_display = ('name', 'department', 'start_time', 'end_time')
	list_filter = ['name']

admin.site.register(Shift, ShiftAdmin);