from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .views import update_database_by_phone


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    update_database_by_phone(user.username)
