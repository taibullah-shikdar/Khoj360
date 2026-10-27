from .models import NearbyNews


def notification_counts(request):
    if not request.user.is_authenticated:
        return {
            "unread_notification_count": 0,
            "unread_emergency_count": 0,
            "unread_medical_count": 0,
            "unread_repair_count": 0,
            "unseen_news_count": 0,
        }

    unread_notifications = request.user.notifications.filter(is_read=False)
    seen_ids = request.user.seen_news.values_list("id", flat=True)
    unseen_news = NearbyNews.objects.filter(is_active=True).exclude(id__in=seen_ids).count()

    # "Emergency SOS" title → Emergency badge
    emergency_count = unread_notifications.filter(title__icontains="Emergency SOS").count()
    # "Medical" title → Medical badge (Emergency, Blood, Organ)
    medical_count = unread_notifications.filter(title__icontains="Medical").count()
    # "Repair" title → Repair badge
    repair_count = unread_notifications.filter(title__icontains="Repair").count()


    return {
        "unread_notification_count": unread_notifications.count(),
        "unread_emergency_count": emergency_count,
        "unread_medical_count": medical_count,
        "unread_repair_count": repair_count,
        "unseen_news_count": unseen_news,
    }