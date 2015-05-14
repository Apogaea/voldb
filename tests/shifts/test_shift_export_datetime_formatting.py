from volunteer.apps.shifts.utils import DENVER_TIMEZONE
from volunteer.apps.shifts.export import (
    dt_to_gdocs_date,
    dt_to_gdocs_time,
)
from django.utils import timezone


def test_date_formatting():
    when = timezone.now().astimezone(DENVER_TIMEZONE).replace(
        year=2015, month=11, day=29,
    ).astimezone(timezone.utc)
    assert dt_to_gdocs_date(when) == '2015/29/11'


def test_time_formatting():
    when = timezone.now().astimezone(DENVER_TIMEZONE).replace(
        hour=20, minute=15, second=0,
    ).astimezone(timezone.utc)
    assert dt_to_gdocs_time(when) == '20:15'
