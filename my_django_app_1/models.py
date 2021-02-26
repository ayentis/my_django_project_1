from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
    # username = models.CharField(max_length=12)
    # pass_data = models.DateTimeField(auto_now_add=True)

# class User(models.Model):
#
#     id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
#     password = models.CharField(max_length=20,)
#     pass_data = models.DateTimeField(auto_now_add=True)
#     active = models.BooleanField(default=False)
#     username = models.CharField(max_length=100)


class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)


class RequestHistory(models.Model):
    customerID = models.ForeignKey(Customer, on_delete=models.PROTECT)
    event_data = models.DateTimeField(auto_now_add=True)
    request_name = models.CharField(max_length=100)
    result = models.CharField(max_length=250)


class UpdateHistory(models.Model):
    customerID = models.ForeignKey(Customer, on_delete=models.PROTECT)
    event_data = models.DateTimeField(auto_now_add=True)
    update_data = models.JSONField()
    result = models.CharField(max_length=200)