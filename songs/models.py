# songs/models.py
from django.db import models
from django.contrib.auth.models import User

class Genre(models.TextChoices):
    POP = "pop", "Pop"
    ROCK = "rock", "Rock"
    CLASSICAL = "classical", "Classical"
    HIPHOP = "hiphop", "Hip-Hop"
    JAZZ = "jazz", "Jazz"
    FOLK = "folk", "Folk"
    BLUES = "blues", "Blues"
    RNB = "rnb", "R&B"
    ELECTRONIC = "electronic", "Electronic"
    METAL = "metal", "Metal"
    COUNTRY = "country", "Country"
    REGGAE = "reggae", "Reggae"

class Language(models.TextChoices):
    ENGLISH = "en", "English"
    HINDI = "hi", "Hindi"
    PUNJABI = "pa", "Punjabi"
    TAMIL = "ta", "Tamil"
    TELUGU = "te", "Telugu"
    BENGALI = "bn", "Bengali"
    MARATHI = "mr", "Marathi"
    GUJARATI = "gu", "Gujarati"
    KANNADA = "kn", "Kannada"
    MALAYALAM = "ml", "Malayalam"

class Artist(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200)
    genre = models.CharField(
        max_length=32,
        choices=Genre.choices,
        default=Genre.POP
    )
    language = models.CharField(
        max_length=8,
        choices=Language.choices,
        default=Language.ENGLISH
    )
    artists = models.ManyToManyField(Artist, related_name="songs")
    image = models.ImageField(upload_to="song_images/")
    description = models.TextField(blank=True)
    audio = models.FileField(upload_to="songs/")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_songs")
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self):
        return self.name
