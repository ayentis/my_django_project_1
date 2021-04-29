from django.apps import AppConfig


class MyDjangoApp1Config(AppConfig):
    name = 'my_django_app_1'

    def ready(self):
        from . import signals

