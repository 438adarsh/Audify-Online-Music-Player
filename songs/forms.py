# songs/forms.py
from django import forms
from .models import Song, Artist

class SongForm(forms.ModelForm):
    new_artist = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Add new artist"})
    )

    class Meta:
        model = Song
        fields = ["name", "genre", "language", "artists", "new_artist", "image", "description", "audio"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "genre": forms.Select(attrs={"class": "form-select"}),   # ✅ fixed
            "language": forms.Select(attrs={"class": "form-select"}),
            "artists": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "audio": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
