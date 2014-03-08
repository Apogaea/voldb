from django.contrib import admin
from shifts.models import Shift


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'start_time', 'shift_length', 'owner')
    list_filter = ['shift_length', 'department', 'start_time']

admin.site.register(Shift, ShiftAdmin)
