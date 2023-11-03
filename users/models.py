from django.contrib.auth.models import AbstractUser, User
from django.db import models

from vinilboard.models import Album


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='users_photo/%Y/%m/', null=True, blank=True, verbose_name='Аватар')


class FavoriteAlbums(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
