# accounts/admin.py
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "can_upload", "requested_upload")
    list_filter = ("can_upload", "requested_upload")
    search_fields = ("user__username", "user__email")
