from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile
from core.models import Notification

from .forms import MedicalReportForm, MedicalRequestForm
from .models import MedicalRequest


@login_required
def create_request(request):
    if request.method == "POST":
        form = MedicalRequestForm(request.POST)
        if form.is_valid():
            medical_request = form.save(commit=False)
            medical_request.requester = request.user
            medical_request.is_public = True  # সব request type public — list এ দেখাবে
            medical_request.save()

            # সব medical request (Emergency, Blood, Organ) এর জন্যই Notification তৈরি হবে (navbar এর Medical-এ ব্যাজ আসবে)
            all_users = get_user_model().objects.all()
            req_type_label = dict(MedicalRequest.TYPE_CHOICES).get(medical_request.request_type, "Medical")
            Notification.objects.bulk_create(
                [
                    Notification(
                        user=u,
                        title=f"Medical {req_type_label}",
                        message=f"Medical {req_type_label.lower()} request at {medical_request.location}: {medical_request.description or 'Assistance needed'}",
                        is_read=False,
                    )
                    for u in all_users
                ]
            )

            # হোম পেজে রিডাইরেক্ট করা হলো যাতে ইউজার ন্যাভবারে Medical ব্যাজটি দেখতে পারে
            return redirect("core:home")
    else:
        form = MedicalRequestForm()
    return render(request, "medical/request_form.html", {"form": form, "title": "Create medical request"})


@login_required
def create_sos(request):
    profile = getattr(request.user, "profile", None)
    location = profile.area if profile and profile.area else "Location not provided"
    phone = profile.phone if profile else ""
    medical_request = MedicalRequest.objects.create(
        requester=request.user,
        request_type=MedicalRequest.TYPE_EMERGENCY,
        description="SOS emergency request",
        phone=phone,
        location=location,
        needed_at=timezone.now(),
        is_public=True,
    )
    all_users = get_user_model().objects.all()
    Notification.objects.bulk_create(
        [
            Notification(
                user=u,
                title="Medical Emergency",
                message=f"SOS medical emergency at {location}",
                is_read=False,
            )
            for u in all_users
        ]
    )
    return redirect("core:home")


@login_required
def open_requests(request):
    # Medical সেকশনে আসলে medical নোটিফিকেশনগুলো read হয়ে যাবে এবং ব্যাজ চলে যাবে
    request.user.notifications.filter(is_read=False, title__icontains="Medical").update(is_read=True)

    request_type = request.GET.get("type", "all")
    requests = MedicalRequest.objects.filter(
        is_public=True,
        status=MedicalRequest.STATUS_OPEN,
    )
    if request_type in {MedicalRequest.TYPE_BLOOD, MedicalRequest.TYPE_ORGAN, MedicalRequest.TYPE_EMERGENCY}:
        requests = requests.filter(request_type=request_type)
    elif request_type == "medical":
        requests = requests.filter(request_type=MedicalRequest.TYPE_EMERGENCY)

    emergency_count = MedicalRequest.objects.filter(
        is_public=True,
        status=MedicalRequest.STATUS_OPEN,
        request_type=MedicalRequest.TYPE_EMERGENCY,
    ).count()

    profile = getattr(request.user, "profile", None)
    selected_request = None
    selected_pk = request.GET.get("selected")
    if selected_pk:
        selected_request = requests.filter(pk=selected_pk).first()
    if selected_request is None:
        selected_request = requests.first()

    # নিজের রিকোয়েস্ট নিজে অ্যাকসেপ্ট করতে পারবে না (requester != request.user)
    for medical_request in requests:
        medical_request.can_accept = bool(
            profile
            and medical_request.requester != request.user
            and (
                (medical_request.request_type == MedicalRequest.TYPE_BLOOD and profile.is_donor)
                or (medical_request.request_type != MedicalRequest.TYPE_BLOOD and profile.is_volunteer)
            )
        )
    selected_can_accept = bool(selected_request and getattr(selected_request, "can_accept", False))
    return render(
        request,
        "medical/open_requests.html",
        {
            "requests": requests,
            "selected_request": selected_request,
            "selected_can_accept": selected_can_accept,
            "active_type": request_type,
            "emergency_count": emergency_count,
            "selected_is_own": bool(selected_request and selected_request.requester == request.user),
        },
    )


@login_required
def my_requests(request):
    request.user.notifications.filter(is_read=False, title__icontains="Medical").update(is_read=True)
    requests = MedicalRequest.objects.filter(requester=request.user)
    return render(request, "medical/my_requests.html", {"requests": requests})


@login_required
def accept_request(request, pk):
    medical_request = get_object_or_404(MedicalRequest, pk=pk, is_public=True, status=MedicalRequest.STATUS_OPEN)
    profile = getattr(request.user, "profile", None)
    can_accept = bool(
        profile
        and medical_request.requester != request.user
        and (
            (medical_request.request_type == MedicalRequest.TYPE_BLOOD and profile.is_donor)
            or (medical_request.request_type != MedicalRequest.TYPE_BLOOD and profile.is_volunteer)
        )
    )
    if request.method == "POST" and can_accept:
        medical_request.accepted_by = request.user
        medical_request.status = MedicalRequest.STATUS_ACCEPTED
        medical_request.save()
    return redirect("medical:open_requests")


@login_required
def report_request(request, pk):
    medical_request = get_object_or_404(MedicalRequest, pk=pk, is_public=True)
    if request.method == "POST":
        form = MedicalReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.request = medical_request
            report.reporter = request.user
            report.save()
            return redirect("medical:open_requests")
    else:
        form = MedicalReportForm()
    return render(request, "medical/report_form.html", {"form": form, "medical_request": medical_request})