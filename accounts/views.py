# accounts/views.py
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from .models import Profile
from songs.models import Song

@login_required
def profile_view(request):
    profile = request.user.profile
    user_songs = Song.objects.filter(uploaded_by=request.user)
    
    pending_profiles = None
    if request.user.is_superuser or request.user.email == "pandeypankaj3030@gmail.com":
        pending_profiles = Profile.objects.filter(requested_upload=True, can_upload=False)

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "user_songs": user_songs,
        "pending_profiles": pending_profiles
    })


def is_admin(user):
    return user.is_superuser or user.email == "pandeypankaj3030@gmail.com"

@login_required
@user_passes_test(is_admin)
def manage_requests(request):
    pending_profiles = Profile.objects.filter(requested_upload=True, can_upload=False)
    return render(request, "accounts/manage_requests.html", {"pending_profiles": pending_profiles})

@login_required
@user_passes_test(is_admin)
def approve_request(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.can_upload = True
    profile.requested_upload = False
    profile.save()
    messages.success(request, f"Upload access granted to {profile.user.username}")
    return redirect("accounts:profile")

@login_required
@user_passes_test(is_admin)
def deny_request(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.requested_upload = False
    profile.save()
    messages.info(request, f"Upload request denied for {profile.user.username}")
    return redirect("accounts:profile")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("songs:home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created. Please log in.")
        return redirect("accounts:login")
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("songs:home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("songs:home")
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("accounts:login")

@login_required
def request_upload_access(request):
    profile = request.user.profile
    if not profile.requested_upload and not profile.can_upload:
        profile.requested_upload = True
        profile.save()
        messages.success(request, "Your request to upload songs has been sent.")
    else:
        messages.info(request, "Request already sent or access already granted.")
    return redirect("accounts:profile")

# Admin approves requests (staff only)
@user_passes_test(lambda u: u.is_staff)
def pending_requests(request):
    pending = Profile.objects.filter(requested_upload=True, can_upload=False)
    return render(request, "accounts/pending_requests.html", {"pending": pending})
