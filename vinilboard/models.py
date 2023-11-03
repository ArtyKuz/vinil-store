from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg, QuerySet
from django.urls import reverse


class Genre(models.Model):
    genre = models.CharField(max_length=50, db_index=True, verbose_name='Стиль')
    slug = models.SlugField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre': self.slug})

    class Meta:
        verbose_name_plural = 'Стили'
        verbose_name = 'Стиль'


class Artist(models.Model):
    artist = models.CharField(max_length=50, db_index=True, verbose_name='Исполнитель')
    slug = models.SlugField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return self.artist

    def get_absolute_url(self):
        return reverse('artist', kwargs={'artist': self.slug})

    class Meta:
        verbose_name_plural = 'Исполнители'
        verbose_name = 'Исполнитель'
        ordering = ['artist']


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='albums')
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    year = models.IntegerField(verbose_name='Год выпуска')
    label = models.CharField(max_length=100, verbose_name='Лэйбл')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name='Стиль', related_name='albums')
    price = models.IntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='photos/', verbose_name='Обложка')
    in_stock = models.PositiveIntegerField(default=0, verbose_name='В наличии')
    # orders = models.ManyToManyField('Order', through='OrderAlbum', blank=True)

    class Meta:
        verbose_name_plural = 'Альбомы'
        verbose_name = 'Альбом'
        ordering = ['id']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('album', kwargs={'album': self.slug})

    def get_comments(self):
        return Comment.objects.filter(album=self).select_related('user')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    order_albums = models.ManyToManyField(Album, verbose_name='Альбомы', related_name='orders')
    shipping_address = models.CharField(max_length=200, verbose_name='Адрес доставки')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа')
    date_created_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return f'Заказ № {self.pk}'

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


# class OrderAlbum(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     album = models.ForeignKey(Album, on_delete=models.CASCADE)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # def __str__(self):
    #     return f'{self.quantity} x {self.album}'


class Comment(models.Model):
    class MarkChoice(models.IntegerChoices):
        ONE = 1, '⭐'
        TWO = 2, '⭐⭐'
        THREE = 3, '⭐⭐⭐'
        FOUR = 4, '⭐⭐⭐⭐'
        FIVE = 5, '⭐⭐⭐⭐⭐'

    content = models.CharField(max_length=1000)
    mark = models.IntegerField(choices=MarkChoice.choices, default=MarkChoice.ONE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date_create = models.DateTimeField(auto_now_add=True)






