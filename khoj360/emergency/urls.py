from django.urls import path

from . import views


app_name = "emergency"

urlpatterns = [
    path("", views.sos_home, name="sos_home"),
    path("trigger/", views.trigger_sos, name="trigger_sos"),
]
