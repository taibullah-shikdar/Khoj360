from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from medical.models import MedicalRequest
from repair.models import RepairRequest

from .models import Hotline, NearbyNews


def home(request):
    open_medical_requests = MedicalRequest.objects.filter(
        is_public=True,
        status=MedicalRequest.STATUS_OPEN,
    ).exclude(request_type=MedicalRequest.TYPE_EMERGENCY).exclude(description__icontains="SOS")[:2]
    open_repair_requests = RepairRequest.objects.filter(status=RepairRequest.STATUS_OPEN)[:1]
    news_items = NearbyNews.objects.filter(is_active=True)[:5]

    # Count unseen news for logged-in user
    unseen_news_count = 0
    if request.user.is_authenticated:
        seen_ids = request.user.seen_news.values_list("id", flat=True)
        unseen_news_count = NearbyNews.objects.filter(is_active=True).exclude(id__in=seen_ids).count()

    context = {
        "hotlines": Hotline.objects.filter(is_active=True),
        "news_items": news_items,
        "open_medical_count": MedicalRequest.objects.filter(
            is_public=True, status=MedicalRequest.STATUS_OPEN
        ).exclude(request_type=MedicalRequest.TYPE_EMERGENCY).exclude(description__icontains="SOS").count(),
        "open_repair_count": RepairRequest.objects.filter(status=RepairRequest.STATUS_OPEN).count(),
        "open_medical_requests": open_medical_requests,
        "open_repair_requests": open_repair_requests,
        "unseen_news_count": unseen_news_count,
    }
    return render(request, "core/home.html", context)


def news_list(request):
    """Full nearby news page."""
    news_items = NearbyNews.objects.filter(is_active=True)

    # Mark all as seen for logged-in user
    if request.user.is_authenticated:
        for news in news_items:
            news.seen_by.add(request.user)

    context = {
        "news_items": news_items,
    }
    return render(request, "core/news_list.html", context)


@login_required
def news_add(request):
    """Add a new nearby news item."""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        area = request.POST.get("area", "").strip()
        body = request.POST.get("body", "").strip()
        if title and body:
            NearbyNews.objects.create(
                title=title,
                area=area,
                body=body,
                posted_by=request.user,
                is_active=True,
            )
        # হোম পেজে রিডাইরেক্ট করা হলো যাতে ন্যাভবারে News ব্যাজ দেখা যায়
        return redirect("core:home")
    return render(request, "core/news_add.html", {})



@login_required
def news_delete(request, pk):
    """Delete a news item — only by poster or staff."""
    news = get_object_or_404(NearbyNews, pk=pk)
    if request.user == news.posted_by or request.user.is_staff:
        news.delete()
    return redirect("core:news_list")


@login_required
def notification_count(request):
    unread_notifications = request.user.notifications.filter(is_read=False)
    seen_ids = request.user.seen_news.values_list("id", flat=True)
    unseen_news = NearbyNews.objects.filter(is_active=True).exclude(id__in=seen_ids).count()
    return JsonResponse(
        {
            "count": unread_notifications.count(),
            "emergency_count": unread_notifications.filter(title__icontains="Emergency SOS").count(),
            "medical_count": unread_notifications.filter(title__icontains="Medical").count(),
            "repair_count": unread_notifications.filter(title__icontains="Repair").count(),
            "news_count": unseen_news,
        }
    )

