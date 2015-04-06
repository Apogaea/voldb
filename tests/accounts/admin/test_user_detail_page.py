from django.core.urlresolvers import reverse


def test_user_detail_page(admin_webtest_client):
    url = reverse('admin:user-detail', kwargs={'pk': admin_webtest_client.user.pk})
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_user_editing(admin_webtest_client, factories, User):
    user = factories.UserFactory(
        is_active=False,
        _profile__has_ticket=False,
        is_staff=False,
    )

    url = reverse('admin:user-detail', kwargs={'pk': user.pk})
    response = admin_webtest_client.get(url)
    assert response.status_code == 200

    new_values = {
        'email': 'test-update@example.com',
        'full_name': 'test-full_name',
        'display_name': 'test-display_name',
        'phone': '555-666-7777',
        'has_ticket': True,
        'is_active': True,
        'is_staff': True,
    }

    for k, v in new_values.items():
        response.form[k] = v

    form_response = response.form.submit()
    assert form_response.status_code == 302

    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.email == new_values['email']
    assert updated_user.is_staff == new_values['is_staff']
    assert updated_user.is_active == new_values['is_active']
    assert updated_user.profile.has_ticket == new_values['has_ticket']
    assert updated_user.profile.display_name == new_values['display_name']
    assert updated_user.profile.full_name == new_values['full_name']
    assert updated_user.profile.phone == new_values['phone']
