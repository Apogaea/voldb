from django.core.urlresolvers import reverse


def test_user_list_page(admin_webtest_client):
    url = reverse('admin:user-list')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200
