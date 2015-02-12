from django.contrib import admin
from shifts.models import Shift
from shifts.models import Role
from datetime import timedelta
from django.db.models import F


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'name')
    list_filter = ['department', 'name', 'description']


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'start_time', 'shift_length', 'owner', 'code')
    list_filter = ['shift_length', 'role', 'code', 'start_time']
    actions = ['clear_code', 'advance_time', 'reverse_time', 'add_hour', 'remove_hour']

    def clear_code(self, request, queryset):
        rows_updated = queryset.update(code='')
        if rows_updated == 1:
            message_bit = "1 code was"
        else:
            message_bit = "%s codes were" % rows_updated
        self.message_user(request, "%s cleared." % message_bit)
    clear_code.short_description = "Clear codes for selected shifts"

    def advance_time(self, request, queryset):
        rows_updated = queryset.update(start_time=F('start_time') + timedelta(hours=1))
        if rows_updated == 1:
            message_bit = "1 shift was"
        else:
            message_bit = "%s shifts were" % rows_updated
        self.message_user(request, "%s shifted forward." % message_bit)
    advance_time.short_description = "Shift codes ahead 1 hour"

    def reverse_time(self, request, queryset):
        rows_updated = queryset.update(start_time=F('start_time') + timedelta(hours=-1))
        if rows_updated == 1:
            message_bit = "1 shift was"
        else:
            message_bit = "%s shifts were" % rows_updated
        self.message_user(request, "%s shifted back." % message_bit)
    reverse_time.short_description = "Shift codes back 1 hour"

    def add_hour(self, request, queryset):
        rows_updated = queryset.update(shift_length=F('shift_length') + 1)
        if rows_updated == 1:
            message_bit = "1 shift was"
        else:
            message_bit = "%s shifts were" % rows_updated
        self.message_user(request, "%s lengthened." % message_bit)
    add_hour.short_description = "1 hour longer"

    def remove_hour(self, request, queryset):
        rows_updated = queryset.update(shift_length=F('shift_length') - 1)
        if rows_updated == 1:
            message_bit = "1 shift was"
        else:
            message_bit = "%s shifts were" % rows_updated
        self.message_user(request, "%s shortened." % message_bit)
    remove_hour.short_description = "1 hour shorter"


admin.site.register(Shift, ShiftAdmin)
admin.site.register(Role, RoleAdmin)
