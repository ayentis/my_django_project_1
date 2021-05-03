from django.urls import path
# from .views import maindata, docdata, updatedata, historydata, update_database, send_pass
import my_django_app_1.views as v

urlpatterns = [

    path('send_pass/', v.send_pass),
    path('', v.maindata),
    path('doc/', v.docdata),
    path('update/', v.updatedata),
    path('history/', v.historydata),
    path('update_database/', v.update_database),
    path('current_profile/', v.update_profile)
    # path('login/', registration),


]