from django.utils import timezone


def test_start_time_in_morning(models_no_db):
    shift = models_no_db.Shift(
        start_time=timezone.now().replace(hour=6, minute=30),
    )
    assert shift.get_start_time_display() == '06:30'


def test_start_time_in_afternoon(models_no_db):
    shift = models_no_db.Shift(
        start_time=timezone.now().replace(hour=18, minute=30),
    )
    assert shift.get_start_time_display() == '18:30'
