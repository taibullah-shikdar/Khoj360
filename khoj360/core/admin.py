from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Hotline, NearbyNews, Notification


@admin.register(Hotline)
class HotlineAdmin(admin.ModelAdmin):
    list_display = ("title", "phone", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("title", "phone", "description")


@admin.register(NearbyNews)
class NearbyNewsAdmin(admin.ModelAdmin):
    list_display = ("title", "area", "is_active", "created_at")
    list_filter = ("is_active", "area")
    search_fields = ("title", "area", "body")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("user__username", "title", "message")

# Register your models here.