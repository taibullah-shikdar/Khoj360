from django.contrib import admin

from .models import Profile, VolunteerApplication


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "phone",
        "area",
        "blood_group",
        "is_available",
        "is_volunteer",
        "is_donor",
        "is_repair_provider",
    )
    list_filter = ("is_available", "is_volunteer", "is_donor", "is_repair_provider", "blood_group")
    search_fields = ("user__username", "full_name", "phone", "area")


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "status", "created_at", "updated_at")
    list_filter = ("role", "status")
    search_fields = ("user__username", "message")
    actions = ("approve_applications", "reject_applications")

    @admin.action(description="Approve selected applications")
    def approve_applications(self, request, queryset):
        for application in queryset:
            application.status = VolunteerApplication.STATUS_APPROVED
            application.reviewed_by = request.user
            application.save()

    @admin.action(description="Reject selected applications")
    def reject_applications(self, request, queryset):
        queryset.update(status=VolunteerApplication.STATUS_REJECTED, reviewed_by=request.user)

# Register your models here.
