import operator
import itertools
import functools
import datetime

from django.utils import timezone
from django.utils.datastructures import OrderedDict

DENVER_TIMEZONE = timezone.get_default_timezone()


def pairwise(iterable):
    """
    from python itertools examples: http://docs.python.org/2/library/itertools.html

    iterate through an iterable as pairs
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def check_if_overlap(left, right):
    left_end_time = left['start_time'] + datetime.timedelta(hours=left['shift_length'])
    right_end_time = right['start_time'] + datetime.timedelta(hours=right['shift_length'])

    if left_end_time <= right['start_time']:
        return False
    elif left['start_time'] >= right_end_time:
        return False
    return True


def check_if_midnight_spanning(shift):
    if shift['shift_length'] > 24:
        return True
    start_hour = shift['start_time'].astimezone(DENVER_TIMEZONE).hour
    end_time = shift['start_time'] + datetime.timedelta(hours=shift['shift_length'])
    end_hour = end_time.astimezone(DENVER_TIMEZONE).hour
    return bool(end_hour) and start_hour > end_hour


def build_empty_column(start_time):
    end_time = start_time + datetime.timedelta(hours=1)
    return {
        'columns': 1,
        'open_on_left': False,
        'open_on_right': False,
        'start_time': start_time,
        'end_time': end_time,
        'shift_length': 1,
        'shifts': [],
    }


def build_shift_column(shifts, shift_date):
    is_midnight_spanning = check_if_midnight_spanning(shifts[0])
    start_time = shifts[0]['start_time']
    shift_length = shifts[0]['shift_length']
    end_time = start_time + datetime.timedelta(hours=shift_length)
    open_on_left = False
    open_on_right = False

    if is_midnight_spanning:
        if start_time.astimezone(DENVER_TIMEZONE).date() == shift_date:
            open_on_right = True
            columns = 24 - start_time.astimezone(DENVER_TIMEZONE).hour
        elif end_time.astimezone(DENVER_TIMEZONE).date() == shift_date:
            open_on_left = True
            columns = end_time.astimezone(DENVER_TIMEZONE).hour
        else:
            raise ValueError('Shift does not appear to start or end on the '
                             'provided date')
    else:
        columns = shift_length

    return {
        'columns': columns,
        'open_on_left': open_on_left,
        'open_on_right': open_on_right,
        'start_time': start_time.astimezone(DENVER_TIMEZONE),
        'end_time': end_time.astimezone(DENVER_TIMEZONE),
        'shift_length': shift_length,
        'shifts': [shift['id'] for shift in shifts],
    }


def get_num_columns(data):
    return sum(item['columns'] for item in data)


def shifts_to_non_overlapping_rows(shifts):
    """
    Given a list of shifts, return them in groups, where each group is a list
    of shifts.  When a shift doesn't overlap with any other one, this list will
    be a single shift.
    """
    flattened_shifts = flatten_identical_shifts(shifts)
    shifts = zip(*flattened_shifts.values())[0]
    while shifts:
        overlappers = []
        shifts = sorted(shifts, key=operator.itemgetter('start_time'), reverse=True)

        def extract_non_overlappers(shifts):
            while shifts:
                anchor = shifts.pop()
                while shifts and check_if_overlap(shifts[-1], anchor):
                    overlappers.append(shifts.pop())
                yield anchor

        yield list(
            flattened_shifts[(s['start_time'], s['shift_length'])]
            for s in extract_non_overlappers(shifts)
        )

        shifts = overlappers


def flatten_identical_shifts(shifts):
    # we use an OrderedDict to preserve the order of the shifts.
    grouped = OrderedDict()

    for shift in shifts:
        key = (shift['start_time'], shift['shift_length'])
        if key in grouped:
            grouped[key].append(shift)
        else:
            grouped[key] = [shift]

    return grouped


def shifts_to_tabular_data(grouped_shifts, date):
    """
    Given a row of equal length shifts for a single department and day, returns
    a data structure suitable for outputting them in a tabular data structure.
    """
    data = []

    for shift_group in grouped_shifts:
        # grab a representitive shift.
        shift = shift_group[0]
        if shift['start_time'].astimezone(DENVER_TIMEZONE).date() == date:
            current_hour = get_num_columns(data)
            for i in range(current_hour, shift['start_time'].astimezone(DENVER_TIMEZONE).hour):
                data.append(build_empty_column(datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=i,
                    minute=0,
                    second=0,
                    microsecond=0
                )))
        column = build_shift_column(
            shifts=shift_group,
            shift_date=date,
        )
        if get_num_columns(data) != column['start_time'].hour:
            if not column['open_on_left']:
                raise ValueError("Misplaced Shift")

        data.append(column)

    while get_num_columns(data) < 24:
        start_time = datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=get_num_columns(data),
            minute=0,
            second=0,
            microsecond=0,
        )
        data.append(build_empty_column(start_time))

    return data


def shifts_as_grid(shifts):
    """
    Given a list of shifts, returns them sorted and grouped by

    date -> department -> role > length -> start time
    """
    length_getter = operator.itemgetter('shift_length')

    overall_sort_key = lambda s: (
        s['shift_length'],
        s['start_time'].astimezone(DENVER_TIMEZONE),
    )

    dates = sorted(
        set(
            shift.start_time.astimezone(DENVER_TIMEZONE).date() for shift in shifts
        ) | set(
            shift.end_time.astimezone(DENVER_TIMEZONE).date() for shift in shifts
        )
    )

    shift_data = shifts.values(
        'id', 'start_time', 'shift_length',
    )

    def shift_intersects_date(date, shift):
        end_time = shift['start_time'] + datetime.timedelta(hours=shift['shift_length'])
        if shift['start_time'].astimezone(DENVER_TIMEZONE).date() == date:
            return True
        if end_time.astimezone(DENVER_TIMEZONE).date() == date:
            if end_time.astimezone(DENVER_TIMEZONE).hour == 0:
                return False
            return True
        return False

    for date in dates:
        shifts_by_date = sorted(filter(
            functools.partial(shift_intersects_date, date),
            shift_data,
        ), key=overall_sort_key)
        length_groups = itertools.groupby(shifts_by_date, length_getter)
        for length, shifts_by_length in length_groups:
            for shift_row in shifts_to_non_overlapping_rows(shifts_by_length):
                yield {
                    'date': date,
                    'length': length,
                    'grid': shifts_to_tabular_data(
                        shift_row,
                        date,
                    ),
                }