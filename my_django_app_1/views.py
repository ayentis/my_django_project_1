# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("HELLO WORLD.")
    return render(request, "index.html")

#test


