import urllib

from django.core.urlresolvers import reverse

from shifts.utils import shifts_as_grid
from shifts.factories import (
    today_at_hour, yesterday_at_hour,
)


def test_grid_view(api_client, factories, models):
    """
    - 2 hour shifts, staggered on the hour (1 hour overlap)
    - 4 hour shifts with 1 hour overlap (maybe for a lead role)

    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                [*-*X*-*X*-*X*-*X*-*]
                  [*-*X*-*X*-*X*-*X*-*]
    """
    factories.ShiftFactory(start_time=today_at_hour(6), shift_length=2)
    factories.ShiftFactory(start_time=today_at_hour(7), shift_length=2)

    factories.ShiftFactory(start_time=today_at_hour(8), shift_length=2)
    factories.ShiftFactory(start_time=today_at_hour(9), shift_length=2)

    factories.ShiftFactory(start_time=today_at_hour(10), shift_length=2)
    factories.ShiftFactory(start_time=today_at_hour(11), shift_length=2)

    factories.ShiftFactory(start_time=today_at_hour(12), shift_length=2)
    factories.ShiftFactory(start_time=today_at_hour(13), shift_length=2)

    factories.ShiftFactory(start_time=today_at_hour(14), shift_length=2)
    factories.ShiftFactory(start_time=today_at_hour(15), shift_length=2)

    factories.ShiftFactory(start_time=today_at_hour(6), shift_length=4)
    factories.ShiftFactory(start_time=today_at_hour(9), shift_length=4)
    factories.ShiftFactory(start_time=today_at_hour(12), shift_length=4)

    # Tomorrow
    factories.ShiftFactory(start_time=yesterday_at_hour(23), shift_length=7)
    factories.ShiftFactory(start_time=today_at_hour(5), shift_length=7)
    factories.ShiftFactory(start_time=today_at_hour(11), shift_length=7)
    factories.ShiftFactory(start_time=today_at_hour(17), shift_length=7)

    grid_url = '{0}?{1}'.format(
        reverse('v2:shift-grid'),
        urllib.urlencode(
            [('s', pk) for pk in models.Shift.objects.values_list('pk', flat=True)],
        ),
    )

    response = api_client.get(grid_url)
    assert response.status_code == 200

    expected = tuple(shifts_as_grid(models.Shift.objects.all()))
    actual = response.data

    assert actual == expected
