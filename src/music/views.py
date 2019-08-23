from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import UserForm, LogInForm
from .models import Album, Song


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    login_url = 'music:login'

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user).order_by('-is_favourite', 'id')

    def get_context_data(self, **kwargs):
        """ Checks whether the last letter of the user's first name is an "s", in which case
        it has to write "___s' albums" instead of "___'s albums". """
        context = super(IndexView, self).get_context_data()
        user = self.request.user

        first_name = user.first_name
        if first_name[len(first_name)-1] == "s":
            context['first_name_albums'] = user.first_name + "' " + "albums:"
        else:
            context['first_name_albums'] = user.first_name + "'s " + "albums:"
        return context


class DetailView(generic.DetailView):
    template_name = 'music/detail.html'
    model = Album

    def get_context_data(self, **kwargs):
        """ The "all_albums" attribute in "detail.html" is given the artist's other albums,
        where the album's User field is the same as the request's User ID.
        However, this also excludes the album where the title is equal to the one on this page
         - thus, providing us with the artist's other albums."""

        context = super(DetailView, self).get_context_data(**kwargs)
        album = self.object
        user_albums = Album.objects.filter(user=self.request.user)
        context["all_albums"] = user_albums.filter(artist=album.artist).exclude(title=album.title)
        return context


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']

    def form_valid(self, form):
        """ Overriding form_valid, which does the form saving. Here, we get the "user" who is
        currently logged in and assign the album to them, before we save the album."""
        user = self.request.user
        form.instance.user = user
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


def favourite_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.is_favourite = not album.is_favourite
    album.save()
    return redirect(request.META.get('HTTP_REFERER'))


def favourite_song(request, album_id, song_id):
    album = Album.objects.get(pk=album_id)
    song = album.song_set.get(pk=song_id)
    song.is_favourite = not song.is_favourite
    song.save()
    return redirect(request.META.get('HTTP_REFERER'))


def search_albums(request):
    query = request.GET.get("q")
    album_list = Album.objects.filter(user=request.user).filter(Q(title__contains=query))
    return render(request, 'music/index.html', {
        'all_albums': album_list,
        'search': True,
        'query': query})


class SongCreate(CreateView):
    model = Song
    fields = ['title', 'audio_file']

    def form_valid(self, form):
        album = Album.objects.get(pk=self.kwargs['album_id'])
        form.instance.album = album
        return super(SongCreate, self).form_valid(form)


class SongDelete(DeleteView):
    model = Song

    def get_success_url(self):
        album = self.object.album
        return reverse_lazy('music:detail', kwargs={'pk': album.id})


class SongView(generic.ListView):
    template_name = 'music/songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        song_ids = []
        for album in Album.objects.filter(user=self.request.user):
            for song in album.song_set.all():
                song_ids.append(song.pk)
        song_list = Song.objects.filter(pk__in=song_ids)

        # See if the query is empty (if so, just order all songs with favourite songs first
        # If not, filter the songs according to the query (this does not take into account
        # letter case) and then order with favourite songs first.
        try:
            query = self.request.GET.get("s")
            song_list = song_list.filter(Q(title__icontains=query)).order_by('-is_favourite', 'id')
            return song_list
        except ValueError:
            return Song.objects.all().order_by('-is_favourite', 'id')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # Display blank form to new user
    def get(self, request):

        if request.user.is_authenticated:
            return redirect('music:index')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Cleaned (formatted) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Return User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


class LogInView(LoginView):
    template_name = 'music/login.html'
    success_url = 'music:index'


def logout_user(request):
    logout(request)
    return redirect('music:index')
