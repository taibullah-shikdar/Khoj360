from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignupForm, VolunteerApplicationForm
from .models import Profile, VolunteerApplication


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data.get("phone", ""),
                area=form.cleaned_data.get("area", ""),
                blood_group=form.cleaned_data.get("blood_group", ""),
            )
            login(request, user)
            return redirect("core:home")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={"full_name": request.user.get_full_name() or request.user.username},
    )
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile_obj)
    applications = VolunteerApplication.objects.filter(user=request.user)
    return render(request, "accounts/profile.html", {"form": form, "applications": applications})


@login_required
def apply_role(request):
    if request.method == "POST":
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect("accounts:application_status")
    else:
        form = VolunteerApplicationForm()
    return render(request, "accounts/apply_role.html", {"form": form})


@login_required
def application_status(request):
    applications = VolunteerApplication.objects.filter(user=request.user)
    return render(request, "accounts/application_status.html", {"applications": applications})

# Create your views here.
