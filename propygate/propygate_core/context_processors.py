
import random

from django.conf import settings


def propygate_core(request):

    return {
        'VERSION': settings.VERSION,
        'STATIC_URL': settings.STATIC_URL,
        'DEBUG': settings.DEBUG,
        'STATIC_VERSION': random.random() if settings.DEBUG else settings.VERSION
    }