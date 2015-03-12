def test_profile_created_for_new_user(User, models):
    assert not models.Profile.objects.exists()

    user = User.objects.create(email='test@example.com')

    assert models.Profile.objects.exists()
    assert user.profile
