import pytest


@pytest.fixture()  # NOQA
def webtest_client(db):
    from django_webtest import WebTest

    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app
