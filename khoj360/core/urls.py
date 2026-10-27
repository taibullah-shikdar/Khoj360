from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("news/", views.news_list, name="news_list"),
    path("news/add/", views.news_add, name="news_add"),
    path("news/<int:pk>/delete/", views.news_delete, name="news_delete"),
    path("notifications/count/", views.notification_count, name="notification_count"),
]
