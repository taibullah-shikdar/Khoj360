from django.urls import path

from . import views


app_name = "repair"

urlpatterns = [
    path("new/", views.create_request, name="create_request"),
    path("open/", views.open_requests, name="open_requests"),
    path("mine/", views.my_requests, name="my_requests"),
    path("<int:pk>/accept/", views.accept_request, name="accept_request"),
    path("<int:pk>/done/", views.mark_done, name="mark_done"),
    path("<int:pk>/confirm/", views.confirm_done, name="confirm_done"),
]
