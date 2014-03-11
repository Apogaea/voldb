import operator
import itertools
import functools

from django.utils import timezone

EMPTY_COLUMN = {
    'columns': 1,
    'class': 'empty',
    'is_empty': True,
}

DENVER_TIMEZONE = timezone.get_default_timezone()


def build_multi_shift_column(shifts):
    """
    This function takes a list of shifts which would overlap and returns a data
    structure suitable for rendering them as an inner table in the shifts grid.
    """
    start_hour = shifts[0].start_time.astimezone(DENVER_TIMEZONE).hour
    end_hour = shifts[-1].end_time.astimezone(DENVER_TIMEZONE).hour

    inner_column_builder = functools.partial(
        build_inner_shift_column,
        start_hour=start_hour, end_hour=end_hour,
    )

    return {
        'columns': end_hour - start_hour,
        'class': 'shifts',
        'has_many': True,
        'shifts': map(inner_column_builder, shifts),
    }


def build_single_shift_column(shift):
    """
    Takes a single `shift` instance and builds a data structure suitable for
    outputing it in a tabular data structure.
    """
    return {
        'columns': shift.shift_length,
        'class': 'shift',
        'id': shift.id,
        'owner': shift.owner,
        'start_at': shift.start_time.astimezone(DENVER_TIMEZONE),
    }


def build_inner_shift_column(shift, start_hour, end_hour):
    """
    This builds the inner column data for displaying shifts in an inner table
    in the shifts grid.
    """
    data = []

    for i in range(start_hour, shift.start_time.astimezone(DENVER_TIMEZONE).hour):
        data.append(EMPTY_COLUMN)

    data.append(build_single_shift_column(shift))

    for i in range(shift.end_time.astimezone(DENVER_TIMEZONE).hour, end_hour):
        data.append(EMPTY_COLUMN)

    return data


def get_num_columns(data):
    return sum(item['columns'] for item in data)


def group_overlapping_shifts(shifts):
    """
    Given a list of shifts, return them in groups, where each group is a list
    of shifts.  When a shift doesn't overlap with any other one, this list will
    be a single shift.
    """
    shifts = sorted(shifts, key=operator.attrgetter('start_time'), reverse=True)

    def yield_while_overlapping(shifts):
        prev = None
        while shifts:
            shift = shifts.pop()
            if prev is None:
                yield shift
            elif shift.overlaps_with(prev):
                yield shift
            else:
                shifts.append(shift)
                break
            prev = shift

    while shifts:
        yield list(yield_while_overlapping(shifts))


def shifts_to_tabular_data(shifts):
    """
    Given a row of equal length shifts for a single department and day, returns
    a data structure suitable for outputting them in a tabular data structure.
    """
    data = []

    shift_groups = group_overlapping_shifts(shifts)

    for shift_group in shift_groups:
        current_hour = get_num_columns(data)
        for i in range(current_hour, shift_group[0].start_time.astimezone(DENVER_TIMEZONE).hour):
            data.append(EMPTY_COLUMN)
        if len(shift_group) == 1:
            data.append(build_single_shift_column(shift_group[0]))
        else:
            data.append(build_multi_shift_column(shift_group))

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
                yield {
                    'date': date,
                    'department': department,
                    'length': length,
                    'tabular': shifts_to_tabular_data(shifts_by_length),
                }
