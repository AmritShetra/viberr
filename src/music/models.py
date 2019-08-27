from django.contrib.auth.models import Permission, User
from django.db import models
from django.urls import reverse


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    logo = models.FileField()
    is_favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def get_number_of_songs(self):
        return self.song_set.count()

    def __str__(self):
        return self.title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    audio_file = models.FileField(default='')
    title = models.CharField(max_length=250)
    is_favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.album.pk})

    def __str__(self):
        return self.title + ' - ' + self.album.artist
