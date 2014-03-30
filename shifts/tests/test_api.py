import mock

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.http.request import HttpRequest

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import UserFactory

from shifts.models import Shift
from shifts.factories import ShiftFactory
from shifts.serializers import ShiftSerializer


class ClaimShiftAPITest(APITestCase):
    def test_claim_endpoint_requires_authentication(self):
        shift = ShiftFactory()
        url = reverse('shift-detail', kwargs={'pk': shift.pk})

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            response.data,
        )


def dummy_request(user=None):
    if user is None:
        user = AnonymousUser()
    return mock.Mock(spec=HttpRequest, user=user)


class SerializerTest(TestCase):
    def test_claiming_unclaimed_shift(self):
        user = UserFactory()

        shift = ShiftFactory()

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': user.pk},
            context={'request': dummy_request(user)},
        )
        self.assertTrue(serializer.is_valid())

        updated_shift = serializer.save()
        self.assertEqual(updated_shift.owner, user)

    def test_releasing_claimed_shift(self):
        user = UserFactory()

        shift = ShiftFactory(owner=user)

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': None},
            context={'request': dummy_request(user)},
        )
        self.assertTrue(serializer.is_valid())

        updated_shift = serializer.save()
        self.assertIsNone(updated_shift.owner)

    def test_claiming_shift_with_code(self):
        user = UserFactory()

        shift = ShiftFactory(code='secret')

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': user.pk, 'verification_code': shift.code},
            context={'request': dummy_request(user)},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_shift = serializer.save()
        self.assertEqual(updated_shift.owner, user)

    def test_releasing_shift_with_code(self):
        user = UserFactory()

        shift = ShiftFactory(owner=user, code='secret')

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': None},
            context={'request': dummy_request(user)},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_shift = serializer.save()
        self.assertIsNone(updated_shift.owner)

    def test_releasing_someone_elses_shift(self):
        user = UserFactory()
        other_user = UserFactory()

        shift = ShiftFactory(owner=other_user)

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': None},
            context={'request': dummy_request(user)},
        )
        self.assertFalse(serializer.is_valid())

        self.assertIn('owner', serializer.errors, serializer.errors)
        self.assertIn(
            ShiftSerializer.custom_error_messages['unable_to_release'],
            serializer.errors['owner'],
            serializer.errors,
        )

    def test_claiming_already_claimed_shift(self):
        user = UserFactory()
        other_user = UserFactory()

        shift = ShiftFactory(owner=other_user)

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': user.pk},
            context={'request': dummy_request(user)},
        )
        self.assertFalse(serializer.is_valid())

        self.assertIn('owner', serializer.errors, serializer.errors)
        self.assertIn(
            ShiftSerializer.custom_error_messages['already_claimed'],
            serializer.errors['owner'],
            serializer.errors,
        )

    def test_attempt_to_claim_using_other_users_id(self):
        user = UserFactory()
        other_user = UserFactory()

        shift = ShiftFactory()

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': other_user.pk},
            context={'request': dummy_request(user)},
        )
        self.assertFalse(serializer.is_valid())

        self.assertIn('owner', serializer.errors, serializer.errors)
        self.assertIn(
            ShiftSerializer.custom_error_messages['suspicious_owner'],
            serializer.errors['owner'],
            serializer.errors,
        )

    def test_attempt_to_claim_shift_that_requires_code(self):
        user = UserFactory()

        shift = ShiftFactory(code='secret')

        serializer = ShiftSerializer(
            instance=shift,
            data={'owner': user.pk},
            context={'request': dummy_request(user)},
        )
        self.assertFalse(serializer.is_valid())

        self.assertIn('non_field_errors', serializer.errors, serializer.errors)
        self.assertIn(
            ShiftSerializer.custom_error_messages['invalid_code'],
            serializer.errors['non_field_errors'],
            serializer.errors,
        )
