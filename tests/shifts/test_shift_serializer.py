from volunteer.apps.shifts.serializers import ShiftSerializer


def test_claiming_unclaimed_shift(factories, rf):
    user = factories.UserFactory()
    shift = factories.ShiftFactory()
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': user.pk},
        context={'request': request},
    )
    assert serializer.is_valid()

    updated_shift = serializer.save()
    assert updated_shift.owner == user

def test_releasing_claimed_shift(factories, rf):
    user = factories.UserFactory()
    shift = factories.ShiftFactory(owner=user)
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': None},
        context={'request': request},
    )
    assert serializer.is_valid()

    updated_shift = serializer.save()
    assert updated_shift.owner is None

def test_claiming_shift_with_code(factories, rf):
    user = factories.UserFactory()
    shift = factories.ShiftFactory(code='secret')
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': user.pk, 'verification_code': shift.code},
        context={'request': request},
    )
    assert serializer.is_valid(), serializer.errors

    updated_shift = serializer.save()
    assert updated_shift.owner == user


def test_releasing_shift_with_code(factories, rf):
    user = factories.UserFactory()
    shift = factories.ShiftFactory(owner=user, code='secret')
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': None},
        context={'request': request},
    )
    assert serializer.is_valid(), serializer.errors

    updated_shift = serializer.save()
    assert updated_shift.owner is None


def test_releasing_someone_elses_shift(factories, rf):
    user = factories.UserFactory()
    other_user = factories.UserFactory()

    shift = factories.ShiftFactory(owner=other_user)
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': None},
        context={'request': request},
    )
    assert not serializer.is_valid()

    assert 'owner' in serializer.errors, serializer.errors
    expected_msg = ShiftSerializer.custom_error_messages['unable_to_release']
    assert expected_msg in serializer.errors['owner'], serializer.errors


def test_claiming_already_claimed_shift(factories, rf):
    user = factories.UserFactory()
    other_user = factories.UserFactory()
    request = rf.post('/shifts/1/')
    request.user = user

    shift = factories.ShiftFactory(owner=other_user)

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': user.pk},
        context={'request': request},
    )
    assert not serializer.is_valid()

    assert 'owner' in serializer.errors, serializer.errors
    expected_msg = ShiftSerializer.custom_error_messages['already_claimed']
    assert expected_msg in serializer.errors['owner'], serializer.errors


def test_attempt_to_claim_using_other_users_id(factories, rf):
    user = factories.UserFactory()
    other_user = factories.UserFactory()
    shift = factories.ShiftFactory()
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': other_user.pk},
        context={'request': request},
    )
    assert not serializer.is_valid()

    assert 'owner' in serializer.errors, serializer.errors
    expected_msg = ShiftSerializer.custom_error_messages['suspicious_owner']
    assert expected_msg in serializer.errors['owner'], serializer.errors


def test_attempt_to_claim_shift_that_requires_code(factories, rf):
    user = factories.UserFactory()
    shift = factories.ShiftFactory(code='secret')
    request = rf.post('/shifts/1/')
    request.user = user

    serializer = ShiftSerializer(
        instance=shift,
        data={'owner': user.pk},
        context={'request': request},
    )
    assert not serializer.is_valid()

    assert 'non_field_errors' in serializer.errors, serializer.errors
    expected_msg = ShiftSerializer.custom_error_messages['invalid_code']
    assert expected_msg in serializer.errors['owner'], serializer.errors
