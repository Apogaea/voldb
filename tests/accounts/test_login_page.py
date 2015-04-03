from django.core.urlresolvers import reverse

from rest_framework import status


def test_page_load(webtest_client):
    url = reverse("login")
    response = webtest_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_good_credentials(user, webtest_client):
    assert user.check_password('password')
    url = reverse("login")
    response = webtest_client.get(url)

    response.form['username'] = user.email
    response.form['password'] = 'password'

    expected_location = reverse('dashboard')

    login_response = response.form.submit()
    assert login_response.status_code == status.HTTP_302_FOUND
    assert login_response.location.endswith(expected_location)


def test_bad_credentials(user, webtest_client):
    assert not user.check_password('bad password')
    url = reverse("login")
    response = webtest_client.get(url)

    response.form['username'] = user.email
    response.form['password'] = 'bad password'

    login_response = response.form.submit()
    assert login_response.status_code == status.HTTP_200_OK
