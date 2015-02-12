import pytest

from rest_framework.test import APIClient


@pytest.fixture()  # NOQA
def webtest_client(db):
    from django_webtest import WebTest

    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app


@pytest.fixture()  # NOQA
def factories(db):
    import factory

    from departments.factories import (  # NOQA
        DepartmentFactory,
    )
    from shifts.factories import (  # NOQA
        RoleFactory,
        ShiftFactory,
    )
    from accounts.factories import (  # NOQA
        UserFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.Factory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(db):
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


@pytest.fixture()
def user(django_user_model):
    try:
        user = django_user_model.objects.get(
            email='user@example.com',
        )
    except django_user_model.DoesNotExist:
        user = django_user_model.objects.create(
            email='user@example.com',
            password='password',
        )

    return user


@pytest.fixture()
def api_client(user, db):
    """
    A rest_framework api test client not auth'd.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    client.user = user
    return client
