# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from .models import User, Customer, UpdateHistory, RequestHistory

import json

def index(request):

    # obj, created = User.get_or_create_user_by_login('0665858126')
    if not User.exist_by_login('0665858127'):
        obj, created = User.create_by_phone('0665858127')

        if created:
            obj = User.update_by_login('0665858127', {'email':'ay@gmail.com'})
    else:
        obj = User.get_by_login('ay@gmail.com')

    customer_id = '123'

    for c_obj in obj:
        if not Customer.exist_by_id(customer_id):
            Customer.create({'customer_name': 'vasya', 'id': customer_id, 'user': c_obj})
        else:
            Customer.update_by_id(customer_id, {'customer_name': 'vasya123'})

    cust_obj = Customer.get_by_id(customer_id)

    for c_cust_obj in cust_obj:
        rez1 = RequestHistory.create({'customerID': c_cust_obj, 'request_name': 'r1'})
        rez2 = UpdateHistory.create({'customerID': c_cust_obj, 'update_data': json.dumps({'4': 5, '6': 7})})

    customer_id = '1234'
    cust_obj = Customer.get_by_id(customer_id)

    for c_obj in obj:
        if not Customer.exist_by_id(customer_id):
            Customer.create({'customer_name': 'vasya', 'id': customer_id, 'user': c_obj})
        else:
            Customer.update_by_id(customer_id, {'customer_name': 'vasya1234'})

    for c_cust_obj in cust_obj:
        rez3 = RequestHistory.create({'customerID':c_cust_obj, 'request_name':'r2'})
        rez4 = UpdateHistory.create({'customerID': c_cust_obj, 'update_data': json.dumps({'8': 9, '10': 11})})

    # return HttpResponse(obj)

    rh = RequestHistory.objects.all()
    context = {'rh': rh}

    return render(request, "index.html", context)


def registration(request):
    return render(request, "registration.html", {})


def sendpass(request):
    return render(request, "sendpass.html", {})


def maindata(request):
    return render(request, "basedatamain.html", {})


def docdata(request):
    return render(request, "basedatadoc.html", {})


def updatedata(request):
    return render(request, "basedataupdate.html", {})


def historydata(request):
    return render(request, "basedatahistory.html", {})