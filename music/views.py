from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Album, Song


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    template_name = 'music/detail.html'
    model = Album


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


def favourite_song(request, album_id, song_id):
    album = Album.objects.get(pk=album_id)
    song = album.song_set.get(pk=song_id)
    song.is_favourite = not song.is_favourite
    song.save()
    return redirect(request.META.get('HTTP_REFERER'))


def search_view(request):
    query = request.GET.get("q")
    album_list = Album.objects.filter(Q(title__contains=query))
    return render(request, 'music/index.html', {
        'all_albums': album_list,
        'search': True,
        'query': query})


class SongCreate(CreateView):
    model = Song
    fields = ['title', 'file_type']

    def form_valid(self, form):
        album = Album.objects.get(pk=self.kwargs['album_id'])
        form.instance.album = album
        return super(SongCreate, self).form_valid(form)


class SongView(generic.ListView):
    template_name = 'music/songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        return Song.objects.all()
