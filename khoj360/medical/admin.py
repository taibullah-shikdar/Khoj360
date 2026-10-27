from django.contrib import admin

from .models import MedicalReport, MedicalRequest


@admin.register(MedicalRequest)
class MedicalRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "request_type", "requester", "location", "status", "is_public", "accepted_by", "created_at")
    list_filter = ("request_type", "status", "is_public", "blood_group")
    search_fields = ("location", "hospital", "description", "requester__username")
    actions = ("make_public", "hide_from_public")

    @admin.action(description="Approve/show selected requests publicly")
    def make_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description="Hide selected requests")
    def hide_from_public(self, request, queryset):
        queryset.update(is_public=False)


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ("request", "reporter", "created_at")
    search_fields = ("reason", "reporter__username")

# Register your models here.