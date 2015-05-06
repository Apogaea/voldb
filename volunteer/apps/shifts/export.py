from __future__ import unicode_literals

import six

from volunteer.apps.shifts.utils import DENVER_TIMEZONE

CSV_HEADERS = (
    "Slot ID",
    "Department ID",
    "Department Name",
    "Role ID",
    "Role Name",
    "Shift ID"
    "Shift Start Time",
    "Shift End Time",
    "Volunteer ID",
    "Volunteer Display Name",
    "Volunteer Full Name",
    "Volunteer Phone Number",
    "Volunteer Email",
)


def shift_slot_to_csv_row(shift_slot):
    values = (
        six.text_type(shift_slot.pk),
        six.text_type(shift_slot.shift.role.department.pk),
        six.text_type(shift_slot.shift.role.department.name),
        six.text_type(shift_slot.shift.role.pk),
        six.text_type(shift_slot.shift.role.name),
        six.text_type(shift_slot.shift.pk),
        six.text_type(shift_slot.shift.start_time.astimezone(DENVER_TIMEZONE)),
        six.text_type(shift_slot.shift.end_time.astimezone(DENVER_TIMEZONE)),
        six.text_type(shift_slot.volunteer.pk),
        six.text_type(shift_slot.volunteer.profile.display_name),
        six.text_type(shift_slot.volunteer.profile.full_name),
        six.text_type(shift_slot.volunteer.profile.phone),
        six.text_type(shift_slot.volunteer.email),
    )
    return dict(zip(CSV_HEADERS, values))
