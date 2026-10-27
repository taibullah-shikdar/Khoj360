from django.conf import settings
from django.db import models


class MedicalRequest(models.Model):
    TYPE_EMERGENCY = "emergency"
    TYPE_BLOOD = "blood"
    TYPE_ORGAN = "organ"
    TYPE_CHOICES = [
        (TYPE_EMERGENCY, "Emergency"),
        (TYPE_BLOOD, "Blood"),
        (TYPE_ORGAN, "Organ"),
    ]

    STATUS_OPEN = "open"
    STATUS_ACCEPTED = "accepted"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DONE, "Done"),
    ]

    BLOOD_GROUPS = [
        ("", "Not needed"),
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="medical_requests")
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=180)
    hospital = models.CharField(max_length=180, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True)
    blood_bags = models.PositiveIntegerField(default=0)
    needed_at = models.DateTimeField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_medical_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.location}"


class MedicalReport(models.Model):
    request = models.ForeignKey(MedicalRequest, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for #{self.request_id} by {self.reporter.username}"

# Create your models here.


