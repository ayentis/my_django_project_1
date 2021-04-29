# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import User, Customer, LocalSettings, UpdateHistory, RequestHistory
import requests


def registration(request):

    return render(request, "registration.html", {})


def numeric_password_generator(pass_len):
    import random

    # chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    chars = '1234567890'
    password = ''
    for i in range(pass_len):
        password += random.choice(chars)
    return password


def send_pass(request):

    content = {"UserDoesNotExist": False,
               'PasswordSent': False}

    if request.method == 'POST':
        content['login'] = request.POST['username']
        customers_data = get_data_from_1c(content['login'], 'LoginValid')
        if (customers_data):

            import datetime

            content['password'] = numeric_password_generator(6)
            content["UserDoesNotExist"] = False
            content["PasswordSent"] = True

            obj, created = User.objects.update_or_create(username=content['login'])
            obj.set_password(content['password'])
            obj.is_active = True
            obj.pass_data = datetime.datetime.now()

            obj.save()
        else:
            content["UserDoesNotExist"] = True

    return render(request, "sendpass.html", content)


def get_data_from_1c(phone, ProcedureName = ''):

    # Может декоратор ???
    record_type = LocalSettings.objects.filter(record_type='1c_method')

    if (ProcedureName == ''):
        ProcedureName = record_type[0].value

    if (record_type):
        body_dict = {
            "method": "ExecuteExternalProcessing",
            "ProcessingName": record_type[0].value,
            "ProcedureName": ProcedureName,
            "PhoneNumber": phone
        }

        response = requests.post('http://1cweb.fusion.mk.ua/fusion/hs/PutData'
                                 , json=body_dict
                                 , auth=('exchangetlc', 'passexchange')
                                 , headers={'Content-type': 'application/json'}
        )
        return response.json()


# def set_customers(customers_data):
#


def update_database_by_phone(phone_number):

    obj, created = User.create_by_phone(phone_number)
    customers_data = get_data_from_1c(phone_number)

    for current_customer in customers_data:
        params = {
            'main_data': current_customer['MainData'],
            'add_data': current_customer['AddData']
        }
        if Customer.exist_by_id(current_customer['ID']):
            Customer.update_by_id(current_customer['ID'], params)
        else:
            params['customer_name, id, user'] = current_customer['Name'], current_customer['ID'], obj
            Customer.create(params)


def set_content(request):
    users_customers = request.user.customers.all()
    content = {
        'customers_list': users_customers,
    }
    if customer_id := request.GET.get('customer'):
        content['customer_selected'] = users_customers.get(id=customer_id)
    return content


@login_required
def update_database(request):
    # update_database_by_phone(request.user.username)
    return request.redirect('/')

@login_required
def maindata(request):

    # update_database_by_phone(request.user.username)

    content = set_content(request)
    content['main_data, add_data'] = [],{}

    if customer_id := request.GET.get('customer'):
        content['main_data'] = request.user.customers.get(id=customer_id).main_data
        content['add_data'] =  request.user.customers.get(id=customer_id).add_data
    return render(request, "basedatamain.html", content)


@login_required
def docdata(request):
    return render(request, "basedatadoc.html", set_content(request))


@login_required
def updatedata(request):
    return render(request, "basedataupdate.html", set_content(request))


@login_required
def historydata(request):
    return render(request, "basedatahistory.html", set_content(request))


def enter(request):
    return render(request, "basedatamain.html", {})