from django.conf import settings
from django.db import models


class EmergencySOS(models.Model):
    STATUS_SENT = "sent"
    STATUS_SEEN = "seen"
    STATUS_RESPONDING = "responding"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_SENT, "Sent"),
        (STATUS_SEEN, "Seen"),
        (STATUS_RESPONDING, "Responding"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emergency_sos")
    full_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    area = models.CharField(max_length=120, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    location_accuracy = models.PositiveIntegerField(null=True, blank=True, help_text="Accuracy in meters")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Emergency SOS"
        verbose_name_plural = "Emergency SOS"

    def __str__(self):
        return f"SOS by {self.user.username} - {self.get_status_display()}"

    @property
    def display_name(self):
        if self.full_name:
            return self.full_name
        profile = getattr(self.user, "profile", None)
        if profile and profile.full_name:
            return profile.full_name
        return self.user.get_full_name() or self.user.username

    @property
    def has_live_location(self):
        return self.latitude is not None and self.longitude is not None

    @property
    def map_url(self):
        if not self.has_live_location:
            return ""
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
