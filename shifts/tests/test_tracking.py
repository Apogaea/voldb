from django.test import TestCase

from accounts.factories import UserFactory

from shifts.models import ShiftHistory
from shifts.factories import ShiftFactory


class TrackingTest(TestCase):
    def test_tracking_only_on_change(self):
        shift = ShiftFactory(owner=UserFactory())

        self.assertFalse(ShiftHistory.objects.exists())

        shift.save()

        self.assertFalse(ShiftHistory.objects.exists())

    def test_tracking_occurs_on_release(self):
        user = UserFactory()
        shift = ShiftFactory(owner=user)

        self.assertFalse(ShiftHistory.objects.exists())

        shift.owner = None
        shift.save()

        self.assertTrue(ShiftHistory.objects.exists())

        entry = shift.history.get()
        self.assertEqual(entry.user, user)
        self.assertEqual(entry.action, ShiftHistory.ACTION_RELEASE)

    def test_tracking_occurs_on_claim(self):
        user = UserFactory()
        shift = ShiftFactory()

        self.assertFalse(ShiftHistory.objects.exists())

        shift.owner = user
        shift.save()

        self.assertTrue(ShiftHistory.objects.exists())

        entry = shift.history.get()
        self.assertEqual(entry.user, user)
        self.assertEqual(entry.action, ShiftHistory.ACTION_CLAIM)
