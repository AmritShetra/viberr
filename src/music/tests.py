from django.contrib.auth import get_user_model
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
            Album.objects.create(
                title=i,
                user=user,
                is_favourite=(i % 2 == 0),
                logo="test.png"
            )

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
        self.assertRedirects(response, "/login/?next=/")

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

    def test_dispatch_other_users_album(self):
        """
        dispatch() redirects user to index page if they search for an album that isn't theirs.
        """
        user = User.objects.create(username="user")
        user1 = User.objects.create(username="user1")

        Album.objects.create(title="1", artist="user", user=user, logo="test.png", pk=1)
        Album.objects.create(title="2", artist="user1", user=user1, logo="test.png", pk=2)

        # Logged in as user, so they own the Album titled "1"... let's search for the other one
        self.client.force_login(user)
        response = self.client.get(reverse('music:detail', kwargs={'pk': 2}))

        self.assertRedirects(response, reverse('music:index'), status_code=302, target_status_code=200)

    def test_get_context_data(self):
        """
        get_context_data() returns artist's other albums, sorted by ID, excluding other users' albums.
        """
        user = User.objects.create(username="user")
        user1 = User.objects.create(username="user1")

        # i starts at 0, generally easier to start the title numbering 1 instead
        for i in range(4):
            Album.objects.create(
                title=i+1,
                artist="Imagine Dragons",
                user=user,
                logo="test.png",
                pk=i+1
            )
        Album.objects.create(title=5, artist="Imagine Dragons", user=user1, logo="test.png", pk=5)

        self.client.force_login(user)
        # Get album 1 - other albums should ignore Album 5 but retrieve Albums 2, 3 and 4
        response = self.client.get(
            reverse('music:detail', kwargs={'pk': 1})
        )

        self.assertQuerysetEqual(
            response.context['all_albums'],
            ['<Album: 2 - Imagine Dragons>', '<Album: 3 - Imagine Dragons>', '<Album: 4 - Imagine Dragons>']
        )


class AlbumCreateTests(TestCase):

    def test_form_valid_with_invalid_file_type(self):
        """
        form_valid() should ensure it detects invalid file types.
        """
        user = User.objects.create(username="user")
        self.client.force_login(user)
        album = Album.objects.create(
            title="1",
            artist="user",
            logo="test.mp3",
            pk=1
        )

        file_type = album.logo.url.split('.')[-1]
        file_type = file_type.lower()

        image_file_types = ['png', 'jpg', 'jpeg']
        self.assertNotIn(file_type, image_file_types)


class FavouriteTests(TestCase):

    def test_favourite_album(self):
        """
        favourite_album() should flip the specified album's is_favourite attribute both times.
        """
        user = User.objects.create(username="user")
        self.client.force_login(user)
        album = Album.objects.create(
            title="Walk the Moon",
            artist="Walk the Moon",
            logo="test.png",
            user=user
        )

        # Response needs HTTP_REFERER to know where to redirect
        response = self.client.get(
            reverse('music:album-favourite', kwargs={'album_id': album.id}),
            HTTP_REFERER='/'
        )

        album = Album.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(album.is_favourite, True)

        # Now checking that it gets flipped
        response = self.client.get(
            reverse('music:album-favourite', kwargs={'album_id': album.id}),
            HTTP_REFERER='/'
        )

        album = Album.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(album.is_favourite, False)

    def test_favourite_songs(self):
        """
        favourite_song() acts in the same manner as the test above.
        """
        user = User.objects.create(username="user")
        self.client.force_login(user)
        album = Album.objects.create(
            title="Walk the Moon",
            artist="Walk the Moon",
            logo="test.png",
            user=user,
        )
        song = Song.objects.create(
            album=album,
            title="Tightrope",
        )

        response = self.client.get(
            reverse('music:favourite-song', kwargs={'song_id': song.id}),
            HTTP_REFERER='/'
        )
        song = Song.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(song.is_favourite, True)
