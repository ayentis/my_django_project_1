# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from numpy.linalg import cond

from .models import User, Customer, LocalSettings, UpdateHistory, RequestHistory
from .forms import AddUserIndo
import requests
from django.utils import timezone

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


def send_SMS_letsads(phone_number, text):
    import xmltodict
    send_sms_data = '<?xml version="1.0" encoding="UTF-8"?>' \
                    '<request>' \
                    '<auth>' \
                    '<login>380503944202</login>' \
                    '<password>689282</password>' \
                    '</auth>' \
                    '     <message>' \
                    '     <from>INAGRO</from>' \
                    '     <text>{}</text>' \
                    '     <recipient>{}</recipient>' \
                    '     </message>' \
                    '</request>'

    answer = requests.post("https://letsads.com/api", data=send_sms_data.format(text, '38' + phone_number))

    return xmltodict.parse(answer.text).get('response')


def send_SMS(phone_number, text, last_SMS_datetime):
    import datetime
    result = {'is_error': False,
              'description': ''}

    required_min_diff = 3600  # 1 hour

    if int((timezone.now() - last_SMS_datetime).total_seconds())< required_min_diff:
        result['description'] = 'SMS has been sent to you within 24 hours'
        result['is_error'] = True
    else:
        sms_sender_result = send_SMS_letsads(phone_number, text)

        if sms_sender_result.get('name') == 'Error':
            result['description'] = sms_sender_result.get('description')
            result['is_error'] = True

    return result


def send_pass(request):

    content = {"UserDoesNotExist": False,
               'PasswordSent': False,
               }

    if request.method == 'POST':
        content['login'] = request.POST['username']
        customers_data = get_data_from_1c(content['login'], 'LoginValid')
        if (customers_data):
            import datetime

            obj, created = User.objects.update_or_create(username=content['login'])

            password = numeric_password_generator(6)
            rez_sms_sender = send_SMS(content['login'], f'Personal landowner access {password}', obj.last_SMS_datetime)
            content.update(rez_sms_sender)
            content["PasswordSent"] = True

            # for test
            content['password'] = password

            if not content['is_error']:
                obj.last_SMS_datetime = timezone.now()

            obj.set_password(password)
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

    content = set_content(request)

    if request.method == "POST":
        form = AddUserIndo(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.data['email']
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']

            user.save()
            url = '/'
            if customer_id := content.get('customer_selected'):
                url += '?customer='+customer_id.id
            return redirect(url)
    else:
        form = AddUserIndo({'first_name':request.user.first_name,
                            'last_name':request.user.last_name,
                            'email': request.user.email
                            })

        template_name = "current_profile.html"
        content['form'] = form

    return render(request, template_name, content)
