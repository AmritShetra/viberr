from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
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
