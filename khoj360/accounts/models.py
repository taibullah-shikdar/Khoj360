from django.conf import settings
from django.db import models


class Profile(models.Model):
    BLOOD_GROUPS = [
        ("", "Unknown"),
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    area = models.CharField(max_length=120, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True)
    is_available = models.BooleanField(default=True)
    is_volunteer = models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    is_repair_provider = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username


class VolunteerApplication(models.Model):
    ROLE_VOLUNTEER = "volunteer"
    ROLE_DONOR = "donor"
    ROLE_REPAIR_PROVIDER = "repair_provider"
    ROLE_CHOICES = [
        (ROLE_VOLUNTEER, "Medical volunteer"),
        (ROLE_DONOR, "Blood donor"),
        (ROLE_REPAIR_PROVIDER, "Repair provider"),
    ]

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.STATUS_APPROVED:
            profile, _ = Profile.objects.get_or_create(
                user=self.user,
                defaults={"full_name": self.user.get_full_name() or self.user.username},
            )
            if self.role == self.ROLE_VOLUNTEER:
                profile.is_volunteer = True
            elif self.role == self.ROLE_DONOR:
                profile.is_donor = True
            elif self.role == self.ROLE_REPAIR_PROVIDER:
                profile.is_repair_provider = True
            profile.save()

# Create your models here.
