# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import User, Customer, LocalSettings, UpdateHistory, RequestHistory
from .forms import AddUserIndo
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


def send_SMS(phone_number, text):

    return False


def send_pass(request):

    content = {"UserDoesNotExist": False,
               'PasswordSent': False}

    if request.method == 'POST':
        content['login'] = request.POST['username']
        customers_data = get_data_from_1c(content['login'], 'LoginValid')
        if (customers_data):

            import datetime

            password = numeric_password_generator(6)
            if not send_SMS(content['login'], f'Personal landowner access {password}'):
                content['password'] = password

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


def update_database_by_phone(phone_number):

    obj, created = User.create_by_phone(phone_number)
    customers_data = get_data_from_1c(phone_number)

    for current_customer in customers_data:
        params = {
            'main_data': current_customer['MainData'],
            'add_data': current_customer['AddData'],
            'documents_list': current_customer['DocumentsList'],
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
        content['add_data'] = request.user.customers.get(id=customer_id).add_data
    return render(request, "basedatamain.html", content)


@login_required
def docdata(request):

    content = set_content(request)
    content['doc_data'] = []
    if customer_id := request.GET.get('customer'):
        content['doc_data'] = request.user.customers.get(id=customer_id).documents_list

    return render(request, "basedatadoc.html", content)


@login_required
def updatedata(request):
    return render(request, "basedataupdate.html", set_content(request))


@login_required
def historydata(request):
    return render(request, "basedatahistory.html", set_content(request))


def enter(request):
    return render(request, "basedatamain.html", {})


def update_profile(request):
    if request.method == "POST":
        form = AddUserIndo(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.data['email']
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']

            user.save()

            return redirect('/')
    else:
        form = AddUserIndo({'first_name':request.user.first_name,
                            'last_name':request.user.last_name,
                            'email': request.user.email
                            })
    return render(request, "current_profile.html", {'form':form})
