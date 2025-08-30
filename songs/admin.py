# songs/admin.py
from django.contrib import admin
from .models import Song, Artist

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "language", "uploaded_by", "uploaded_at")
    list_filter = ("genre", "language", "uploaded_by")
    search_fields = ("name", "artists__name")
