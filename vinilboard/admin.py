from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class AlbumAdmin(admin.ModelAdmin):
    fields = ('artist', 'title', 'year', 'slug', 'photo', 'album_cover', 'label', 'genre', 'price', 'in_stock')
    readonly_fields = ('album_cover',)
    list_display = ('artist', 'title', 'album_cover', 'year', 'genre', 'price', 'in_stock', 'total_price')
    list_display_links = ('title',)
    search_fields = ('artist__artist', 'title', 'year')
    list_filter = ('year', 'artist__artist', 'genre__genre')
    prepopulated_fields = {'slug': ('title', 'year')}
    list_editable = ('price',)
    ordering = ['artist__artist']
    list_per_page = 10
    save_on_top = True

    @admin.display(description="Общая стоимость")
    def total_price(self, album: Album):
        return album.price * album.in_stock

    @admin.display(description='Обложка альбома')
    def album_cover(self, album: Album):
        return mark_safe(f"<img src='{album.photo.url}' width=100>")


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist',)
    list_display_links = ('artist',)
    search_fields = ('artist',)
    prepopulated_fields = {'slug': ('artist',)}
    list_per_page = 15


class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    list_display_links = ('genre',)
    search_fields = ('genre',)
    prepopulated_fields = {'slug': ('genre',)}
    ordering = ('genre',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'total_amount', 'date_created_order')
    filter_horizontal = ('order_albums',)




admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Order, OrderAdmin)
