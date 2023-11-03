import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from vinilboard.models import Artist


class ArtistTestCase(TestCase):

    def setUp(self) -> None:
        self.obj1 = Artist.objects.create(artist='name', slug='name')
        self.user = User.objects.create(username='user1')
        self.user_staff = User.objects.create(username='user2', is_staff=True)

    def test_artists_get(self):
        url = reverse('artist-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_artist_get(self):
        url = reverse('artist-detail', args=[self.obj1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.obj1.id)
        self.assertEqual(response.data['artist'], self.obj1.artist)

    def test_artist_create_not_staff(self):
        url = reverse('artist-list')
        self.client.force_login(self.user)
        data = {'artist': '111', 'slug': '111'}
        response = self.client.post(url, data=data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_artist_create_staff(self):
        url = reverse('artist-list')
        self.client.force_login(self.user_staff)
        data = {'artist': '111', 'slug': '111'}
        response = self.client.post(url, data=data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['artist'], data['artist'])
        self.assertEqual(Artist.objects.all().count(), 2)
