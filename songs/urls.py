# songs/urls.py
from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("upload/", views.song_create, name="song_create"),
    path("<int:pk>/edit/", views.song_update, name="song_update"),
    path("<int:pk>/delete/", views.song_delete, name="song_delete"),
]
