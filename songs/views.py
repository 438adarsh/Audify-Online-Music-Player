# songs/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Song, Artist, Genre, Language
from .forms import SongForm
from .permissions import user_can_upload

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

@login_required
def song_create(request):
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            song.save()
            form.save_m2m()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "html": render(request, "songs/song_form.html", {"form": form}).content.decode("utf-8")})
    else:
        form = SongForm()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, "songs/song_form.html", {"form": form})
        return render(request, "songs/song_form.html", {"form": form})


@login_required
def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk, uploaded_by=request.user)
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({
                "success": False,
                "html": render(request, "songs/song_form.html", {"form": form}).content.decode("utf-8")
            })
    else:
        form = SongForm(instance=song)
        # ✅ Important: return raw HTML, not JSON
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, "songs/song_form.html", {"form": form})
        return render(request, "songs/song_form.html", {"form": form})

@login_required
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if not user_can_upload(request.user) or (not request.user.is_staff and request.user != song.uploaded_by):
        messages.error(request, "Not allowed.")
        return redirect("songs:home")

    if request.method == "POST":
        song.delete()
        messages.success(request, "Song deleted.")
        return redirect("songs:home")

    return render(request, "songs/song_confirm_delete.html", {"song": song})


def songs_view(request):
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("songs")  # refresh after upload
    else:
        form = SongForm()

    context = {
        "song_form": form,
        "profile": request.user.profile,  # assuming Profile model has can_upload
    }
    return render(request, "songs.html", context)


def home_view(request):
    """List + search + filters + Netflix-style cards."""
    q = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "")
    language = request.GET.get("language", "")
    artist_id = request.GET.get("artist", "")

    songs = Song.objects.all()

    if q:
        songs = songs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(artists__name__icontains=q)
        ).distinct()

    if genre:
        songs = songs.filter(genre=genre)
    if language:
        songs = songs.filter(language=language)
    if artist_id:
        songs = songs.filter(artists__id=artist_id)

    # Pagination (optional)
    paginator = Paginator(songs, 24)  # 24 cards per page
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "genres": Genre.choices,
        "languages": Language.choices,
        "artists": Artist.objects.order_by("name"),
        "q": q, "genre": genre, "language": language, "artist_id": artist_id,
    }
    return render(request, "songs/home.html", context)

