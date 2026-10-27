from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile
from core.models import Notification

from .models import EmergencySOS


@login_required
def sos_home(request):

    request.user.notifications.filter(is_read=False, title__icontains="Emergency SOS").update(is_read=True)
    latest_sos = EmergencySOS.objects.filter(user=request.user).first()
    recent_sos = EmergencySOS.objects.select_related("user")[:12]
    return render(
        request,
        "emergency/sos.html",
        {
            "latest_sos": latest_sos,
            "recent_sos": recent_sos,
        },
    )


@login_required
def trigger_sos(request):
    if request.method == "POST":
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={"full_name": request.user.get_full_name() or request.user.username},
        )
        latitude = request.POST.get("latitude") or None
        longitude = request.POST.get("longitude") or None
        location_accuracy = request.POST.get("location_accuracy") or None
        sos = EmergencySOS.objects.create(
            user=request.user,
            full_name=profile.full_name or request.user.get_full_name() or request.user.username,
            phone=profile.phone,
            area=profile.area,
            latitude=latitude,
            longitude=longitude,
            location_accuracy=round(float(location_accuracy)) if location_accuracy else None,
        )

        Notification.objects.create(
            user=request.user,
            title="Emergency SOS sent",
            message=f"Your SOS request #{sos.id} has been sent.",
        )

        all_other_users = get_user_model().objects.exclude(pk=request.user.pk)
        Notification.objects.bulk_create(
            [
                Notification(
                    user=u,
                    title="Emergency SOS",
                    message=f"🚨 {sos.full_name or request.user.username} sent an SOS from {profile.area or 'unknown area'}. Please help!",
                    is_read=False,
                )
                for u in all_other_users
            ]
        )
    return redirect("emergency:sos_home")

