from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage


def environment(**options):
    env = Environment(**options)
    # Add Django-like helpers to Jinja
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
