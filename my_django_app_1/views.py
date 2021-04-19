# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from .models import User, Customer, UpdateHistory, RequestHistory
import requests


def registration(request):

    return render(request, "registration.html", {})


def sendpass(request):
    return render(request, "sendpass.html", {})


def get_data_from_1c(phone):

    body_dict = {
        "method": "ExecuteExternalProcessing",
        "ProcessingName": "GetLandOwnerInfo",
        "ProcedureName": "GetLandOwnerInfo",
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



def update_database(phone_number):

    obj, created = User.create_by_phone(phone_number)
    customers_data = get_data_from_1c(phone_number)

    for current_customer in customers_data:
        Customer.create({
            'customer_name': current_customer['Name'],
            'id': current_customer['ID'],
            'user': obj,
            'main_data': current_customer['MainData'],
            'add_data': current_customer['AddData']
        })

def maindata(request):

    content = {}
    if request.method == 'POST':
        update_database(request.POST['phone'])
        content['customers_list'] = Customer.objects.filter(user__username=request.POST['phone'])
    else:
        print('hello Other ' + request.method, request)

    return render(request, "basedatamain.html", content)


def docdata(request):
    return render(request, "basedatadoc.html", {})


def updatedata(request):
    return render(request, "basedataupdate.html", {})


def historydata(request):
    return render(request, "basedatahistory.html", {})


def enter(request):
    return render(request, "basedatamain.html", {})