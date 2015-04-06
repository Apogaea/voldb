from django.core.urlresolvers import reverse


def test_event_list_page(admin_webtest_client):
    url = reverse('admin:event-create')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200

    response.form['name'] = 'Test Event'
