from __future__ import unicode_literals

import six

import unicodecsv as csv

from django.http import HttpResponse
from django.views.generic import (
    ListView,
)

from django_tables2 import (
    SingleTableMixin,
)

from volunteer.apps.shifts.utils import DENVER_TIMEZONE
from volunteer.apps.shifts.admin.tables import (
    ShiftSlotReportTable,
)
from volunteer.apps.shifts.models import (
    ShiftSlot,
)

CSV_HEADERS = (
    "Slot ID",
    "Department ID",
    "Department Name",
    "Role ID",
    "Role Name",
    "Shift ID",
    "Shift Start Date",
    "Shift Start Time",
    "Shift End Date",
    "Shift End Time",
    "Volunteer ID",
    "Volunteer Display Name",
    "Volunteer Full Name",
    "Volunteer Phone Number",
    "Volunteer Email",
)


def dt_to_gdocs_date(when):
    return when.astimezone(
        DENVER_TIMEZONE,
    ).strftime("%Y/%d/%m")


def dt_to_gdocs_time(when):
    return when.astimezone(
        DENVER_TIMEZONE,
    ).strftime("%H:%M")


def shift_slot_to_csv_row(shift_slot):
    values = (
        six.text_type(shift_slot.pk),
        six.text_type(shift_slot.shift.role.department.pk),
        six.text_type(shift_slot.shift.role.department.name),
        six.text_type(shift_slot.shift.role.pk),
        six.text_type(shift_slot.shift.role.name),
        six.text_type(shift_slot.shift.pk),
        six.text_type(dt_to_gdocs_date(shift_slot.shift.start_time)),
        six.text_type(dt_to_gdocs_time(shift_slot.shift.start_time)),
        six.text_type(dt_to_gdocs_date(shift_slot.shift.end_time)),
        six.text_type(dt_to_gdocs_time(shift_slot.shift.end_time)),
        six.text_type(shift_slot.volunteer.pk),
        six.text_type(shift_slot.volunteer.profile.display_name),
        six.text_type(shift_slot.volunteer.profile.full_name),
        six.text_type(shift_slot.volunteer.profile.phone),
        six.text_type(shift_slot.volunteer.email),
    )
    if len(values) != len(CSV_HEADERS):
        raise ValueError("Length mismatch between data and expected headers")
    return dict(zip(CSV_HEADERS, values))


class ShiftSlotReportView(SingleTableMixin, ListView):
    context_object_name = 'shifts'
    model = ShiftSlot
    table_class = ShiftSlotReportTable

    def return_csv_download(self, *args, **kwargs):
        filename = self.get_filename()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

        writer = csv.DictWriter(response, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for shift_slot in self.get_queryset():
            row = shift_slot_to_csv_row(shift_slot)
            writer.writerow(row)
        return response

    def get(self, *args, **kwargs):
        if 'download' in self.request.GET:
            return self.return_csv_download(*args, **kwargs)
        else:
            return super(ShiftSlotReportView, self).get(*args, **kwargs)

    def get_filename(self):
        raise NotImplementedError("Must implement")

    def get_extra_filters(self):
        raise NotImplementedError("Must be implemented by subclass")

    def get_queryset(self):
        return ShiftSlot.objects.filter(
            cancelled_at__isnull=True,
            **self.get_extra_filters()
        ).filter_to_current_event(
        ).order_by(
            'shift__role__department',
            'shift__role',
            'shift__start_time',
            'shift__shift_minutes',
            'volunteer___profile__display_name',
        ).select_related()
