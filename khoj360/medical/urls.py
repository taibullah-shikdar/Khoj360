from django.urls import path

from . import views


app_name = "medical"

urlpatterns = [
    path("new/", views.create_request, name="create_request"),
    path("sos/", views.create_sos, name="create_sos"),
    path("open/", views.open_requests, name="open_requests"),
    path("mine/", views.my_requests, name="my_requests"),
    path("<int:pk>/accept/", views.accept_request, name="accept_request"),
    path("<int:pk>/report/", views.report_request, name="report_request"),
]