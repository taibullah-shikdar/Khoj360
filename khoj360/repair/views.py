from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from accounts.models import Profile
from core.models import Notification

from .forms import RepairRequestForm
from .models import RepairRequest


@login_required
def create_request(request):
    if request.method == "POST":
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            repair_request = form.save(commit=False)
            repair_request.requester = request.user
            repair_request.save()

            # সব ইউজারদের জন্য Repair Notification তৈরি হবে (navbar এর Repair-এ ব্যাজ আসবে)
            all_users = get_user_model().objects.all()
            Notification.objects.bulk_create(
                [
                    Notification(
                        user=u,
                        title="Repair Request",
                        message=f"New repair request: {repair_request.get_repair_type_display()} repair at {repair_request.location}",
                        is_read=False,
                    )
                    for u in all_users
                ]
            )

            # হোম পেজে রিডাইরেক্ট যাতে ন্যাভবারে Repair ব্যাজটি সাথে সাথে দেখা যায়
            return redirect("core:home")
    else:
        form = RepairRequestForm()
    return render(request, "repair/request_form.html", {"form": form})


@login_required
def open_requests(request):
    # Repair section এ visit করলে repair notifications read হয়ে যাবে — badge চলে যাবে
    request.user.notifications.filter(is_read=False, title__icontains="Repair").update(is_read=True)

    requests = RepairRequest.objects.filter(status=RepairRequest.STATUS_OPEN)
    profile = getattr(request.user, "profile", None)
    is_provider = bool(profile and profile.is_repair_provider)

    for item in requests:
        item.can_accept = bool(is_provider and item.requester != request.user)

    selected_request = None
    selected_pk = request.GET.get("selected")
    if selected_pk:
        selected_request = requests.filter(pk=selected_pk).first()
    if selected_request is None:
        selected_request = requests.first()

    selected_can_accept = bool(selected_request and is_provider and selected_request.requester != request.user)
    selected_is_own = bool(selected_request and selected_request.requester == request.user)

    return render(
        request,
        "repair/open_requests.html",
        {
            "requests": requests,
            "can_accept": is_provider,
            "selected_request": selected_request,
            "selected_can_accept": selected_can_accept,
            "selected_is_own": selected_is_own,
        },
    )


@login_required
def my_requests(request):
    request.user.notifications.filter(is_read=False, title__icontains="Repair").update(is_read=True)
    requests = RepairRequest.objects.filter(requester=request.user)
    return render(request, "repair/my_requests.html", {"requests": requests})



@login_required
def accept_request(request, pk):
    repair_request = get_object_or_404(RepairRequest, pk=pk, status=RepairRequest.STATUS_OPEN)
    profile = getattr(request.user, "profile", None)
    # ইউজার নিজের দেওয়া রিপেয়ার রিকোয়েস্ট নিজে কখনোই অ্যাকসেপ্ট করতে পারবে না
    if request.method == "POST" and profile and profile.is_repair_provider:
        if repair_request.requester != request.user:
            repair_request.accepted_by = request.user
            repair_request.status = RepairRequest.STATUS_ACCEPTED
            repair_request.save()
    return redirect("repair:open_requests")


@login_required
def mark_done(request, pk):
    repair_request = get_object_or_404(RepairRequest, pk=pk, accepted_by=request.user)
    if request.method == "POST":
        repair_request.status = RepairRequest.STATUS_DONE
        repair_request.save()
    return redirect("repair:open_requests")


@login_required
def confirm_done(request, pk):
    repair_request = get_object_or_404(RepairRequest, pk=pk, requester=request.user, status=RepairRequest.STATUS_DONE)
    if request.method == "POST":
        repair_request.status = RepairRequest.STATUS_CONFIRMED
        repair_request.save()
    return redirect("repair:my_requests")
