# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path('upload/', views.request_upload_access, name='request_upload_access'),
    path("manage-requests/", views.manage_requests, name="manage_requests"),
    path("approve-request/<int:profile_id>/", views.approve_request, name="approve_request"),
    path("deny-request/<int:profile_id>/", views.deny_request, name="deny_request"),
]
