import operator


EMPTY_COLUMN = {
    'columns': 1,
}


def build_column_from_shift(shift):
    return {
        'columns': shift.shift_length,
    }


def get_num_columns(data):
    return sum(item['columns'] for item in data)


def shifts_to_tabular_data(shifts):
    data = []
    shifts = sorted(shifts, key=operator.attrgetter('start_time'), reverse=True)

    while get_num_columns(data) < 24:
        current_column = get_num_columns(data)
        if shifts:
            shift = shifts.pop()
            start_column = shift.start_time.hour
            column = build_column_from_shift(shift)
        else:
            start_column = 24
            column = None

        for i in range(current_column, start_column):
            data.append(EMPTY_COLUMN)

        if column:
            data.append(column)

    return data
