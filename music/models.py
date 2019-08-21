from django.db import models
from django.urls import reverse


class Album(models.Model):
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    logo = models.FileField()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    title = models.CharField(max_length=250)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + self.album.artist
