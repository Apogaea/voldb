from volunteer.apps.shifts.context_processors import shift_stats


def test_with_no_slots(request_factory):
    request = request_factory.get('/')
    request.session = {}
    stats = shift_stats(request)
    assert stats


def test_with_a_slot(factories, request_factory):
    request = request_factory.get('/')
    request.session = {}
    factories.ShiftSlotFactory()
    stats = shift_stats(request)
    assert stats
