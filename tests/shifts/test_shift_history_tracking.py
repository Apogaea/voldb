def test_tracking_only_on_change(factories, models):
    shift = factories.ShiftFactory(owner=factories.UserFactory())

    assert not models.ShiftHistory.objects.exists()

    shift.save()

    assert not models.ShiftHistory.objects.exists()


def test_tracking_occurs_on_release(factories, models):
    user = factories.UserFactory()
    shift = factories.ShiftFactory(owner=user)

    assert not models.ShiftHistory.objects.exists()

    shift.owner = None
    shift.save()

    assert models.ShiftHistory.objects.exists()

    entry = shift.history.get()
    assert entry.user == user
    assert entry.action == models.ShiftHistory.ACTION_RELEASE


def test_tracking_occurs_on_claim(factories, models):
    user = factories.UserFactory()
    shift = factories.ShiftFactory()

    assert not models.ShiftHistory.objects.exists()

    shift.owner = user
    shift.save()

    assert models.ShiftHistory.objects.exists()

    entry = shift.history.get()
    assert entry.user == user
    assert entry.action == models.ShiftHistory.ACTION_CLAIM
