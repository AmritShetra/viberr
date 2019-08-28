from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from .models import Album, Song


class TestcaseUserBackend(object):

    def authenticate(self, testcase_user=None):
        return testcase_user

    def get_user(self, user_id):
        User = get_user_model()
        return User.objects.get(pk=user_id)


class AlbumModelTests(TestCase):

    def test_get_number_of_songs_with_zero_songs(self):
        """
        get_number_of_songs() returns 0 with an empty song_set.
        """
        album = Album()
        self.assertEqual(album.get_number_of_songs(), 0)

    def test_get_number_of_songs_with_three_songs(self):
        """
        get_number_of_songs() returns 3 with a song_set of 3 songs.
        """
        user = User.objects.create(username="test")
        album = Album(title="Test Album", user=user)
        album.save()
        i = 0
        while i < 3:
            album.song_set.create(title="Test Song" + str(i))
            i += 1
        self.assertEqual(album.get_number_of_songs(), 3)


class IndexViewTests(TestCase):

    def test_get_queryset(self):
        """
        get_queryset() returns a QuerySet with three albums, ordered by favourites and ID.
        """
        user = User.objects.create(username="test", first_name="Test", last_name="McTest")
        user.set_password("test")
        user.save()

        for i in range(3):
            Album.objects.create(title=i, user=user, is_favourite=(i % 2 == 0), logo="test.png")

        self.client.force_login(user)
        response = self.client.get(reverse('music:index'))
        self.assertQuerysetEqual(
            response.context['all_albums'],
            ['<Album: 0 - >', '<Album: 2 - >', '<Album: 1 - >']
        )

    def test_logged_out(self):
        """
        If the user is not logged in, they are redirected to the "music:login" page.
        """
        response = self.client.get(reverse('music:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/music/login/?next=/music/")

    def test_get_context_data_name_without_s(self):
        """
        get_context_data() returns "Test's albums" if the user's first name is "Test".
        """
        user = User.objects.create(username="test", first_name="Test")
        self.client.force_login(user)
        response = self.client.get(reverse('music:index'))
        self.assertEqual(response.context['first_name_albums'], "Test's albums:")

    def test_get_context_data_name_with_s(self):
        """
        get_context_data() returns "James' albums" if the user's first name is "James".
        """
        user = User.objects.create(username="james", first_name="James")
        self.client.force_login(user)
        response = self.client.get(reverse('music:index'))
        self.assertEqual(response.context['first_name_albums'], "James' albums:")


class DetailViewTests(TestCase):

    def test_get_context_data(self):
        """
        get_context_data() returns artist's other albums, sorted by ID, excluding other users' albums.
        """
        user = User.objects.create(username="user")
        user1 = User.objects.create(username="user1")

        for i in range(4):
            Album.objects.create(title=i+1, artist="Imagine Dragons", user=user, logo="test.png")
        Album.objects.create(title=5, artist="Imagine Dragons", user=user1, logo="test.png")

        self.client.force_login(user)
        response = self.client.get(reverse('music:detail', kwargs={'pk': 2}))
        self.assertQuerysetEqual(
            response.context['all_albums'],
            ['<Album: 2 - Imagine Dragons>', '<Album: 3 - Imagine Dragons>', '<Album: 4 - Imagine Dragons>']
        )
