from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import UserForm
from .models import Album, Song

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class IndexView(LoginRequiredMixin, generic.ListView):
    """Album index view."""
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    # LOGIN_URL in settings.py

    def get_queryset(self):
        """
        Returns the user's albums, ordered by favourites and then IDs.
        """
        return Album.objects.filter(user=self.request.user).order_by('-is_favourite', 'id')

    def get_context_data(self):
        """
        Returns one of two possible strings, depending on if the user's name ends in an "s".
        """
        context = super(IndexView, self).get_context_data()
        user = self.request.user

        first_name = user.first_name
        if not first_name:
            context['first_name_albums'] = "Your albums:"
        else:
            if first_name[len(first_name)-1] == "s":
                context['first_name_albums'] = user.first_name + "' " + "albums:"
            else:
                context['first_name_albums'] = user.first_name + "'s " + "albums:"
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Album detail view."""
    template_name = 'music/detail.html'
    model = Album

    def dispatch(self, request, *args, **kwargs):
        """
        If the album does not belong to this user, redirect them away.
        """
        album = Album.objects.get(id=self.kwargs['pk'])
        user_albums = Album.objects.filter(user=self.request.user)
        album_id_list = []
        for user_album in user_albums:
            album_id_list.append(user_album.id)

        if album.id not in album_id_list:
            return redirect("music:index")
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Gets the artist's other albums, having excluded the one being displayed currently.
        """
        context = super(DetailView, self).get_context_data(**kwargs)
        album = self.object
        user_albums = Album.objects.filter(user=self.request.user)
        context["all_albums"] = user_albums.filter(artist=album.artist).exclude(title=album.title).order_by("id")
        return context


class AlbumCreate(LoginRequiredMixin, CreateView):
    """Album create view."""
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']

    def form_valid(self, form):
        """
        Gets the current user and assigns the album to them.
        Checks if the logo's file type is invalid - if so, refresh and display a blank form.
        """
        user = self.request.user
        form.instance.user = user

        file_type = form.instance.logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            messages.add_message(self.request, messages.INFO, "Invalid file type. Please try again.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    """Edit album view."""
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumDelete(LoginRequiredMixin, DeleteView):
    """Delete album view."""
    model = Album
    success_url = reverse_lazy('music:index')


def favourite_album(request, album_id):
    """
    Flips the given album's "is_favourite" field and returns the user to the previous page.
    """
    if not request.user.is_authenticated:
        return redirect("music:login")
    album = Album.objects.get(pk=album_id)
    album.is_favourite = not album.is_favourite
    album.save()
    return redirect(request.META.get('HTTP_REFERER'))


def favourite_song(request, song_id):
    """
    Same as above.
    """
    if not request.user.is_authenticated:
        return redirect("music:login")
    song = Song.objects.get(pk=song_id)
    song.is_favourite = not song.is_favourite
    song.save()
    return redirect(request.META.get('HTTP_REFERER'))


def search_albums(request):
    """
    Gets the query, filters the Album table from the database and sends them to the main page.
    """
    query = request.GET.get("q")
    album_list = Album.objects.filter(user=request.user).filter(Q(title__contains=query))
    return render(request, 'music/index.html', {
        'all_albums': album_list,
        'search': True,
        'query': query})


class SongCreate(LoginRequiredMixin, CreateView):
    """Create song view."""
    model = Song
    fields = ['title', 'audio_file']

    def form_valid(self, form):
        """
        Assigns the song to the album from the previous page.
        Gets the extension of the audio file's url and redirects to previous page if invalid.
        """
        album = Album.objects.get(pk=self.kwargs['album_id'])
        form.instance.album = album

        file_type = form.instance.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            messages.add_message(self.request, messages.INFO, "Invalid file type. Please try again.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        return super(SongCreate, self).form_valid(form)


class SongUpdate(LoginRequiredMixin, UpdateView):
    """Song edit view."""
    model = Song
    fields = ['title', 'audio_file']


class SongDelete(LoginRequiredMixin, DeleteView):
    """Song delete view."""
    model = Song

    def get_success_url(self):
        """
        On success, take the user back to the album of the song they have just deleted.
        """
        album = self.object.album
        return reverse_lazy('music:detail', kwargs={'pk': album.id})


class SongView(LoginRequiredMixin, generic.ListView):
    """Song list view."""
    template_name = 'music/songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        """
        Get the user's songs from the database, then filter if there is a search.
        """
        # Searches through the database's Album table for the user's albums.
        song_ids = []
        for album in Album.objects.filter(user=self.request.user):
            for song in album.song_set.all():
                # Adds the ID of each song to a list.
                song_ids.append(song.pk)

        # Filters the database for all songs in the above list.
        song_list = Song.objects.filter(pk__in=song_ids)

        # Check the page request for a search query.
        try:
            query = self.request.GET.get("s")
            return song_list.filter(Q(title__icontains=query)).order_by('-is_favourite', 'id')

        # An error is returned if there is no search, so display all songs.
        except ValueError:
            return song_list.order_by('-is_favourite', 'id')


class UserFormView(View):
    """User creation view."""
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        """
        Displays a blank form to a new user.
        """
        if request.user.is_authenticated:
            return redirect('music:index')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Process the form data.
        """
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
    """User login view."""
    template_name = 'music/login.html'
    success_url = 'music:index'
    redirect_authenticated_user = True  # Check settings.py for the LOGIN_REDIRECT_URL (music:index)


class LogOutView(LogoutView):
    """User logout view."""
    next_page = 'music:login'


class UserUpdate(LoginRequiredMixin, UpdateView):
    """User edit view."""
    model = User
    form_class = UserForm
    template_name = 'music/edit_user_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        If the user's ID is not the same as the URL's user ID, redirect them away.
        """
        if self.request.user.id != int(self.kwargs['pk']):
            return redirect("music:index")
        return super(UserUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Saves the user's details into the database.
        User is logged out by default when the password is changed, so reauthenticate them.
        """
        user = form.save(commit=True)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.request.META.get('HTTP_REFERER'))
