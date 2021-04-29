from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


def user_login_valid(user_login):
    from re import compile

    pattern_email = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
    pattern_phone = compile(r'\d{10}$')

    if pattern_email.match(user_login):
        return True, 'email'
    elif pattern_phone.match(user_login):
        return True, 'phone'
    else:
        return False, ''


class User(AbstractUser):

    @staticmethod
    def exist_by_login(user_login):
        return User.objects.filter(Q(username=user_login) | Q(email=user_login)).exists()

    @staticmethod
    def create_by_phone(user_login):
        return User.objects.get_or_create(username=user_login, defaults={'is_active': False})

    @staticmethod
    def update_by_login(user_login, new_value):
        return User.objects.filter(Q(username=user_login) | Q(email=user_login)).update(**new_value)

    @staticmethod
    def get_by_login(user_login):
        return User.objects.filter(Q(username=user_login) | Q(email=user_login))

    pass_data = models.DateTimeField(auto_now_add=True)
    id_external = models.CharField(max_length=36, default='00000000000000000000000000000000022')
    auto_update = models.BooleanField(default=True)

class Customer(models.Model):

    @staticmethod
    def update_by_id(local_id, new_value):
        return Customer.objects.filter(id=local_id).update(**new_value)

    @staticmethod
    def exist_by_id(local_id):
        return Customer.objects.filter(id=local_id).exists()

    @staticmethod
    def create(local_values):
        return Customer.objects.get_or_create(**local_values)

    @staticmethod
    def get_by_id(local_id):
        return Customer.objects.filter(id=local_id)

    customer_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customers')
    id = models.CharField(max_length=38, primary_key=True, unique=True, null=False, blank=False)
    main_data = models.JSONField(null=True)
    add_data = models.JSONField(null=True)

class RequestHistory(models.Model):

    @staticmethod
    def create(local_values):
        return RequestHistory.objects.create(**local_values)

    customerID = models.ForeignKey(Customer, on_delete=models.PROTECT)
    event_data = models.DateTimeField(auto_now_add=True)
    request_name = models.CharField(max_length=100)
    result = models.CharField(max_length=250)


class UpdateHistory(models.Model):

    @staticmethod
    def create(local_values):
        return UpdateHistory.objects.create(**local_values)

    customerID = models.ForeignKey(Customer, on_delete=models.PROTECT)
    event_data = models.DateTimeField(auto_now_add=True)
    update_data = models.JSONField()
    result = models.CharField(max_length=200)


class LocalSettings(models.Model):
    RECORD_TYPES_LIST = (
        (None, 'Select record type'),
        ('1c_path', '1c path'),
        ('1c_method', '1c method'),
        ('1c_user', '1c user'),
        ('1c_password', '1c user password'),
    )

    record_type = models.CharField(max_length=20, choices=RECORD_TYPES_LIST, unique=True)
    value = models.CharField(max_length=250)
