from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.IndexView.as_view(), name='index'),

    # /music/login/
    path('login/', views.LogInView.as_view(), name='login'),

    # /music/logout/
    path('logout', views.LogOutView.as_view(), name='logout'),

    # /music/register/
    path('register/', views.UserFormView.as_view(), name='register'),

    # /music/71/
    path('<pk>/', views.DetailView.as_view(), name='detail'),

    # /music/album/add/
    path('album/add/', views.AlbumCreate.as_view(), name='album-add'),

    # /music/album/71/
    path('album/<pk>/', views.AlbumUpdate.as_view(), name='album-update'),

    # /music/album/71/delete/
    path('album/<pk>/delete/', views.AlbumDelete.as_view(), name='album-delete'),

    # /music/71/favourite/
    path('<album_id>/favourite/', views.favourite_album, name='album-favourite'),

    # /music/songs/2/favourite/
    path('songs/<song_id>/favourite/', views.favourite_song, name='favourite-song'),

    # /music/search/
    path('search/results/', views.search_albums, name='album-search'),

    # /music/71/add/
    path('<album_id>/add/', views.SongCreate.as_view(), name='song-add'),

    # /music/71/2/edit
    path('<album_id>/<pk>/edit/', views.SongUpdate.as_view(), name='song-update'),

    # /music/songs/2/delete/
    path('songs/<pk>/delete/', views.SongDelete.as_view(), name='song-delete'),

    # /music/songs/
    path('songs', views.SongView.as_view(), name='songs'),

    # /music/user/
    path('user/<pk>/edit', views.UserUpdate.as_view(), name='user-edit'),
]
