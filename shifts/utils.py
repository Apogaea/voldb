import operator
import itertools

from django.utils import timezone

EMPTY_COLUMN = {
    'columns': 1,
    'class': 'empty',
}

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


def build_shift_column(shift):
    return {
        'columns': shift.shift_length,
        'class': 'shift',
        'shift': shift,
    }


def get_num_columns(data):
    return sum(item['columns'] for item in data)


def shifts_to_non_overlapping_rows(shifts):
    """
    Given a list of shifts, return them in groups, where each group is a list
    of shifts.  When a shift doesn't overlap with any other one, this list will
    be a single shift.
    """
    while shifts:
        overlappers = []
        shifts = sorted(shifts, key=operator.attrgetter('start_time'), reverse=True)

        def extract_non_overlappers(shifts):
            while shifts:
                anchor = shifts.pop()
                while shifts and shifts[-1].overlaps_with(anchor):
                    overlappers.append(shifts.pop())
                yield anchor

        yield list(extract_non_overlappers(shifts))

        shifts = overlappers


def shifts_to_tabular_data(shifts):
    """
    Given a row of equal length shifts for a single department and day, returns
    a data structure suitable for outputting them in a tabular data structure.
    """
    data = []

    for shift in shifts:
        current_hour = get_num_columns(data)
        for i in range(current_hour, shift.start_time.astimezone(DENVER_TIMEZONE).hour):
            data.append(EMPTY_COLUMN)

        data.append(build_shift_column(shift))

    while get_num_columns(data) < 24:
        data.append(EMPTY_COLUMN)

    return data


def group_shifts(shifts):
    """
    Given a list of shifts, returns them sorted and grouped by

    date -> department -> length -> start time
    """
    date_getter = lambda shift: shift.start_time.astimezone(DENVER_TIMEZONE).date()
    department_getter = lambda shift: shift.department
    length_getter = lambda shift: shift.shift_length

    overall_sort_key = lambda s: (s.start_time.astimezone(DENVER_TIMEZONE).date(), s.department_id, s.shift_length, s.start_time.astimezone(DENVER_TIMEZONE).time())

    shifts = sorted(
        shifts,
        key=overall_sort_key,
    )

    date_groups = itertools.groupby(shifts, date_getter)

    for date, shifts_by_date in date_groups:
        department_groups = itertools.groupby(shifts_by_date, department_getter)
        for department, shifts_by_department in department_groups:
            length_groups = itertools.groupby(shifts_by_department, length_getter)
            for length, shifts_by_length in length_groups:
                for shift_row in shifts_to_non_overlapping_rows(shifts_by_length):
                    yield {
                        'date': date,
                        'department': department,
                        'length': length,
                        'tabular': shifts_to_tabular_data(shift_row),
                    }
