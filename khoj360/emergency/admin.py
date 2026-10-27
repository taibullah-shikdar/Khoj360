from django.contrib import admin

from .models import EmergencySOS


@admin.register(EmergencySOS)
class EmergencySOSAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "phone", "area", "latitude", "longitude", "status", "created_at")
    list_filter = ("status", "area")
    search_fields = ("user__username", "full_name", "phone", "area")
    actions = ("mark_seen", "mark_responding", "mark_resolved")

    @admin.action(description="Mark selected SOS as seen")
    def mark_seen(self, request, queryset):
        queryset.update(status=EmergencySOS.STATUS_SEEN)

    @admin.action(description="Mark selected SOS as responding")
    def mark_responding(self, request, queryset):
        queryset.update(status=EmergencySOS.STATUS_RESPONDING)

    @admin.action(description="Mark selected SOS as resolved")
    def mark_resolved(self, request, queryset):
        queryset.update(status=EmergencySOS.STATUS_RESOLVED)
