import pytest

from django_webtest import (
    WebTest as BaseWebTest,
    DjangoTestApp as BaseDjangoTestApp,
)

from rest_framework.test import APIClient


@pytest.fixture()  # NOQA
def factories(transactional_db):
    import factory

    from tests.factories.events import (  # NOQA
        EventFactory,
        FutureEventFactory,
        PastEventFactory,
    )
    from tests.factories.shifts import (  # NOQA
        ShiftFactory,
        ShiftSlotFactory,
        CancelledShiftSlotFactory,
    )
    from tests.factories.departments import (  # NOQA
        DepartmentFactory,
        RoleFactory,
    )
    from tests.factories.accounts import (  # NOQA
        UserFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.DjangoModelFactory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models_no_db():
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(models_no_db, transactional_db):
    return models_no_db


class DjangoTestApp(BaseDjangoTestApp):
    @property
    def user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = self.session.get('_auth_user_id')
        if user_id:
            return User.objects.get(pk=user_id)
        else:
            return None


class WebTest(BaseWebTest):
    app_class = DjangoTestApp

    def authenticate(self, user):
        self.app.get('/', user=user)

    def unauthenticate(self):
        self.app.get('/', user=None)


@pytest.fixture()  # NOQA
def webtest_client(transactional_db):
    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app


@pytest.fixture()
def user_webtest_client(webtest_client, user):
    web_test = WebTest(methodName='__call__')
    web_test()
    web_test.authenticate(user)
    return web_test.app


@pytest.fixture()
def admin_webtest_client(webtest_client, admin_user):
    web_test = WebTest(methodName='__call__')
    web_test()
    web_test.authenticate(admin_user)
    return web_test.app


@pytest.fixture()  # NOQA
def User(django_user_model):
    """
    A slightly more intuitively named
    `pytest_django.fixtures.django_user_model`
    """
    return django_user_model


@pytest.fixture()
def admin_user(factories, User):
    try:
        return User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        return factories.UserFactory(
            email='admin@example.com',
            is_superuser=True,
            password='password',
        )


@pytest.fixture()
def user(factories, User):
    try:
        return User.objects.get(email='test@example.com')
    except User.DoesNotExist:
        return factories.UserFactory(
            email='test@example.com',
            password='password',
        )


@pytest.fixture()
def user_client(user, client):
    assert client.login(username=user.email, password='password')
    client.user = user
    return client


@pytest.fixture()
def admin_client(admin_user, client):
    assert client.login(username=admin_user.email, password='password')
    client.user = admin_user
    return client


@pytest.fixture()
def api_client(user, db):
    """
    A rest_framework api test client not auth'd.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client
