from django.urls import path

from .views import  registration, sendpass, maindata, docdata, updatedata, historydata

urlpatterns = [
    # path('', views.index, name='index'),
    # path('index/', index),
    path('sendpass/', sendpass),
    path('main/', maindata),
    path('doc/', docdata),
    path('update/', updatedata),
    path('history/', historydata),
    path('', registration),


]