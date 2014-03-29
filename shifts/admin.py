from django.contrib import admin
from shifts.models import Shift


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'start_time', 'shift_length', 'owner', 'code')
    list_filter = ['shift_length', 'department', 'code', 'start_time']
    actions = ['clear_code']

    def clear_code(self, request, queryset):
        rows_updated = queryset.update(code='')
        if rows_updated == 1:
            message_bit = "1 code was"
        else:
            message_bit = "%s codes were" % rows_updated
        self.message_user(request, "%s cleared." % message_bit)
    clear_code.short_description = "Clear codes for selected shifts"

admin.site.register(Shift, ShiftAdmin)