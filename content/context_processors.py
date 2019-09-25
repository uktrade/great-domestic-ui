from django.conf import settings


def get_url(url_name):
    return getattr(settings, url_name, None) or '#'
