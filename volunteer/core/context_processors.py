from django.conf import settings


def rollbar(request):
    if hasattr(settings, 'ROLLBAR'):
        return {
            'ROLLBAR_CONFIG': {
                'accessToken': "544446e12a35497fb539240b854d91b4",
                'captureUncaught': True,
                'payload': {
                    'environment': settings.ROLLBAR['environment'],
                },
            },
        }
    return {}
