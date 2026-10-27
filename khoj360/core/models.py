from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Hotline(models.Model):
    title = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return f"{self.title} - {self.phone}"


class NearbyNews(models.Model):
    title = models.CharField(max_length=160)
    area = models.CharField(max_length=120, blank=True)
    body = models.TextField()
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_posts",
    )
    seen_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="seen_news",
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Nearby news"

    def __str__(self):
        return self.title

    @property
    def unseen_count_for_user(self):
        """Use context — call from view instead."""
        return 0


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=160)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

# Create your models here.
