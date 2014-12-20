import pytest


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
