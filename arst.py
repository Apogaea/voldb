import csv
from dateutil import parser

from django.db import transaction

from volunteer.apps.shifts.models import (
    Shift,
)
from volunteer.apps.departments.models import (
    Department,
)
from volunteer.apps.events.models import (
    Event,
)

headers = (
    'dept',
    'Role',
    'date',
    'duration',
    'code',
)


def load_shift_csv(location='tmp/shift-data.csv'):
    with open(location, 'r') as shift_csv:
        reader = csv.DictReader(shift_csv, fieldnames=headers)
        reader.next()
        return [row for row in reader]


def parse_shift_data(shift_data):
    event = Event.objects.get(name="Apogaea 2015")
    for index, row in enumerate(shift_data):
        if not any(v for v in row.values()):
            continue
        try:
            parse_shift_row(row, event)
        except Exception as e:  # NOQA
            import ipdb; ipdb.set_trace()  # NOQA
            raise


HOUR = 60


def parse_shift_row(row, event):
    missing_fields = set(headers).symmetric_difference(row.keys())
    if missing_fields:
        import ipdb; ipdb.set_trace()  # NOQA
    dept, _ = Department.objects.get_or_create(name=row['dept'])
    start_time = parser.parse(row['date'])
    shift_minutes = HOUR * int(row['duration'])
    code = row['code'].strip()
    role, _ = dept.roles.get_or_create(name=row['Role'])
    return Shift.objects.create(
        event=event,
        start_time=start_time,
        shift_minutes=shift_minutes,
        code=code,
        role=role,
    )


def orchestrate():
    with transaction.atomic():
        data = load_shift_csv()
        parse_shift_data(data)
