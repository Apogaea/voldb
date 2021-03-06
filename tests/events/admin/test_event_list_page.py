from django.core.urlresolvers import reverse


def test_event_list_page(admin_webtest_client, factories):
    factories.EventFactory.create_batch(2)
    url = reverse('admin:event-list')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200
