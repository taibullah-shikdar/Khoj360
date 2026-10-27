from django.contrib import admin

from .models import RepairRequest


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "repair_type", "requester", "location", "budget", "status", "accepted_by", "created_at")
    list_filter = ("repair_type", "status")
    search_fields = ("location", "description", "requester__username", "accepted_by__username")

# Register your models here.
