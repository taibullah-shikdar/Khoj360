from django.conf import settings
from django.db import models
from django.import


class RepairRequest(models.Model):
    TYPE_CAR = "car"
    TYPE_HOME = "home"
    TYPE_CHOICES = [
        (TYPE_CAR, "Car"),
        (TYPE_HOME, "Home"),
    ]

    STATUS_OPEN = "open"
    STATUS_ACCEPTED = "accepted"
    STATUS_DONE = "done"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DONE, "Provider marked done"),
        (STATUS_CONFIRMED, "User confirmed"),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="repair_requests")
    repair_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=180)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_repair_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_repair_type_display()} repair - {self.location}"

# Create your models here.
