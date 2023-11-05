from http import HTTPStatus

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from vinilboard.forms import SearchForm
from vinilboard.models import Genre, Album, Artist


class MainPageTestCase(TestCase):
    fixtures = ['vinilboard_album.json', 'vinilboard_artist.json', 'vinilboard_genre.json']

    def setUp(self) -> None:
        path = reverse('main')
        self.response = self.client.get(path)

    def test_view(self):

        self.assertTemplateUsed(self.response, 'vinilboard/main.html')
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(self.response.context_data['title'], 'Главная страница')
        self.assertIn('search_form', self.response.context_data)

    def test_data_mainpage(self):
        genres = Genre.objects.all()

        self.assertQuerysetEqual(self.response.context_data['object_list'], genres)
        self.assertQuerysetEqual(self.response.context_data['other_genres'], genres[4:])


class CatalogTestCase(TestCase):
    fixtures = ['vinilboard_album.json', 'vinilboard_artist.json', 'vinilboard_genre.json']

    def test_catalog(self):
        albums = Album.objects.all().select_related('artist')
        path = reverse('catalog')
        response = self.client.get(path)

        self.assertTemplateUsed(response, 'vinilboard/catalog.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Каталог')
        self.assertIn('search_form', response.context_data)

        self.assertQuerysetEqual(response.context_data['object_list'], albums[:25])


class ShowGenreTestCase(TestCase):
    fixtures = ['vinilboard_album.json', 'vinilboard_artist.json', 'vinilboard_genre.json']

    def test_genre(self):
        genre = Genre.objects.all().first()
        albums = Album.objects.filter(genre=genre)
        path = reverse('genre', args=[genre.slug])
        response = self.client.get(path)

        self.assertTemplateUsed(response, 'vinilboard/genre.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], genre)
        self.assertIn('search_form', response.context_data)

        self.assertQuerysetEqual(response.context_data['object_list'], albums[:25])


class AlbumTestCase(TestCase):
    fixtures = ['vinilboard_album.json', 'vinilboard_artist.json', 'vinilboard_genre.json']

    def test_album(self):
        album = Album.objects.all().first()
        path = reverse('album', args=[album.slug])
        response = self.client.get(path)

        self.assertTemplateUsed(response, 'vinilboard/album.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], album)
        self.assertIn('search_form', response.context_data)

        self.assertEqual(response.context_data['album'], album)
        self.assertNotIn(album, response.context_data['other_releases'])


class ArtistTestCase(TestCase):
    fixtures = ['vinilboard_album.json', 'vinilboard_artist.json', 'vinilboard_genre.json']

    def test_artist(self):
        artist = Artist.objects.all().first()
        albums = Album.objects.filter(artist=artist)
        path = reverse('artist', args=[artist.slug])
        response = self.client.get(path)
        self.assertTemplateUsed(response, 'vinilboard/artist.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], artist)
        self.assertIn('search_form', response.context_data)

        self.assertQuerysetEqual(response.context_data['albums'], albums)


class SearchTestCase(TestCase):
    fixtures = ['vinilboard_album.json', 'vinilboard_artist.json', 'vinilboard_genre.json']

    def test_search(self):
        keyword = 'Pink Floyd'
        data = {'keyword': keyword}
        albums = Album.objects.filter(Q(title__icontains=keyword) | Q(artist__artist__icontains=keyword))
        path = reverse('search')
        response = self.client.post(path, data)

        self.assertTemplateUsed(response, 'vinilboard/search.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Поиск')
        self.assertIn('search_form', response.context)

        self.assertQuerysetEqual(response.context['page_obj'], albums)


